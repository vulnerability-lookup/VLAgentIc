import requests
from spade_llm import LLMTool

from vlagentic.models.cwe import VLAICWEClassifier


#
# Classify CWE
#


class CWEClassifierTool:
    name = "cwe_classifier"
    description = (
        "Classifies a vulnerability description into CWE categories "
        "and maps them to parent CWEs using the VLAI model."
    )

    def __init__(
        self,
        model_name: str,
        mapping_path: str,
        top_k: int = 5,
    ):
        self.classifier = VLAICWEClassifier(
            model_name=model_name,
            mapping_path=mapping_path,
            top_k=top_k,
        )

    def __call__(self, text: str) -> dict:
        return self.classifier.predict_cwe(text)


_classifier = CWEClassifierTool(
    model_name="CIRCL/cwe-parent-vulnerability-classification-roberta-base",
    mapping_path="data/child_to_parent_mapping.json",
    top_k=5,
)


async def classify_cwe(text: str) -> dict:
    """
    Tool wrapper used by the LLM.
    """
    return _classifier(text)


cwe_classify_tool = LLMTool(
    name="classify_cwe",
    description=(
        "Classify a vulnerability description into CWE categories. "
        "Returns the primary CWE, normalized confidence, and top CWE predictions."
    ),
    parameters={
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "Vulnerability description to classify",
            }
        },
        "required": ["text"],
    },
    func=classify_cwe,
)

#
# Recent Vulnerability per CWE
#


def get_vulnerabilities(cwe_id):
    url = (
        "https://vulnerability.circl.lu/api/vulnerability/"
        f"?source=cvelistv5&cwe={cwe_id.upper()}&sort_order=desc&date_sort=published"
    )
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return [{"error": "Unable to fetch data from Vulnerability Lookup"}]

    vulnerabilities = response.json()
    results = []

    for vuln in vulnerabilities[:3]:
        # Title
        title = vuln.get("title", "No title available")

        # Description (prefer CNA description)
        descriptions = vuln.get("containers", {}).get("cna", {}).get("descriptions", [])
        description = (
            descriptions[0].get("value") if descriptions else "No description available"
        )

        # Vendor / product
        affected = vuln.get("containers", {}).get("cna", {}).get("affected", [])
        if affected:
            vendor = affected[0].get("vendor", "Unknown Vendor")
            product = affected[0].get("product", "Unknown Product")
            vendor_product = f"{vendor} / {product}"
        else:
            vendor_product = "Unknown Vendor/Product"

        # CVE ID + link
        cve_id = vuln.get("cveMetadata", {}).get("cveId", "Unknown CVE")
        link = f"https://vulnerability.circl.lu/vuln/{cve_id}"

        results.append(
            {
                "title": title,
                "description": description,
                "vendor_product": vendor_product,
                "link": link,
            }
        )

    return results


# LLM Tool Wrapper
class VulnerabilityLLMTool:
    name = "vulnerability_info_by_cwe"
    description = (
        "Fetch recent vulnerabilities based on a given CWE ID. "
        "Returns a brief title, description, affected vendor/product, and a link to the Vulnerability Lookup page."
    )

    async def process_request(self, cwe_id: str) -> str:
        vulnerabilities = get_vulnerabilities(cwe_id)
        if "error" in vulnerabilities[0]:
            return vulnerabilities[0]["error"]

        # Construct a readable response for the user
        response = f"Here are the recent vulnerabilities for CWE-{cwe_id}:\n"
        for idx, vuln in enumerate(vulnerabilities, start=1):
            response += f"\n{idx}. **{vuln['title']}**\n"
            response += f"   Description: {vuln['description']}\n"
            response += f"   Affected: {vuln['vendor_product']}\n"
            response += f"   More details: {vuln['link']}\n"

        return response


# Instantiate the tool
vulnerability_per_cwe_tool = LLMTool(
    name="vulnerability_info_by_cwe",
    description=(
        "Fetch recent vulnerabilities based on a given CWE ID. "
        "Returns a brief title, description, affected vendor/product, and a link to the Vulnerability Lookup page."
    ),
    parameters={
        "type": "object",
        "properties": {
            "cwe_id": {
                "type": "string",
                "description": "CWE ID to search for recent vulnerabilities",
            }
        },
        "required": ["cwe_id"],
    },
    func=VulnerabilityLLMTool().process_request,
)

if __name__ == "__main__":
    print(get_vulnerabilities("CWE-119"))

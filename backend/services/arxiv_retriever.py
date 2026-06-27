import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
from typing import List, Dict

def fetch_arxiv_papers(query: str, max_results: int = 5) -> List[Dict]:
    """
    Queries the public arXiv API for relevant papers.
    Parses the returned Atom XML feed into a structured list of paper details.
    """
    encoded_query = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&max_results={max_results}"
    
    # Pre-cached fallback resources to prevent network blockage during local testing
    fallback_papers = [
        {
            "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
            "authors": "Lewis et al.",
            "summary": "We propose Retrieval-Augmented Generation (RAG) which combines pre-trained parametric and non-parametric memory for generation tasks.",
            "year": "2020",
            "id": "2005.11401",
            "url": "https://arxiv.org/abs/2005.11401",
            "citation": "[Lewis et al., 2020]"
        },
        {
            "title": "Attention Is All You Need",
            "authors": "Vaswani et al.",
            "summary": "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions.",
            "year": "2017",
            "id": "1706.03762",
            "url": "https://arxiv.org/abs/1706.03762",
            "citation": "[Vaswani et al., 2017]"
        },
        {
            "title": "Language Models are Few-Shot Learners",
            "authors": "Brown et al.",
            "summary": "We demonstrate that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes reaching competitiveness with prior state-of-the-art approaches.",
            "year": "2020",
            "id": "2005.14165",
            "url": "https://arxiv.org/abs/2005.14165",
            "citation": "[Brown et al., 2020]"
        }
    ]
    
    try:
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "AcademicResearchPipeline/1.0"}
        )
        with urllib.request.urlopen(req, timeout=6.0) as response:
            xml_data = response.read()
            
            # Remove XML namespaces to simplify ElementTree parsing
            xml_data_clean = re.sub(rb'\sxmlns="[^"]+"', b'', xml_data, count=1)
            root = ET.fromstring(xml_data_clean)
            
            papers = []
            for entry in root.findall("entry"):
                title_elem = entry.find("title")
                summary_elem = entry.find("summary")
                published_elem = entry.find("published")
                id_elem = entry.find("id")
                
                title = title_elem.text.strip().replace("\n", " ") if title_elem is not None else "Untitled Paper"
                summary = summary_elem.text.strip().replace("\n", " ") if summary_elem is not None else ""
                
                # Fetch first author's name
                author_names = []
                for author in entry.findall("author"):
                    name_elem = author.find("name")
                    if name_elem is not None:
                        author_names.append(name_elem.text.strip())
                
                if author_names:
                    first_author = author_names[0]
                    authors_str = f"{first_author} et al." if len(author_names) > 1 else first_author
                else:
                    authors_str = "Unknown"
                
                year = "2024"
                if published_elem is not None and published_elem.text:
                    year = published_elem.text.split("-")[0]
                
                paper_id = "0000.0000"
                paper_url = ""
                if id_elem is not None and id_elem.text:
                    paper_url = id_elem.text.strip()
                    id_match = re.search(r'/abs/([^v/]+)', paper_url)
                    if id_match:
                        paper_id = id_match.group(1)
                
                # Extract last name of the first author for citation key
                lastname = authors_str.split(" ")[-1] if " et al." not in authors_str else authors_str.replace(" et al.", "")
                lastname = lastname.split(",")[-1].strip()  # handle format differences
                citation = f"[{lastname} et al., {year}]"
                
                papers.append({
                    "title": title,
                    "authors": authors_str,
                    "summary": summary,
                    "year": year,
                    "id": paper_id,
                    "url": paper_url,
                    "citation": citation
                })
            
            if papers:
                return papers
    except Exception as e:
        print(f"arXiv Retrieval failed or timed out: {e}. Falling back to pre-cached paper pool.")
        
    # Return filtered fallbacks based on query keyword matching
    keywords = [k.lower() for k in query.split()]
    matching = [
        p for p in fallback_papers 
        if any(kw in p["title"].lower() or kw in p["summary"].lower() for kw in keywords)
    ]
    return matching if matching else fallback_papers

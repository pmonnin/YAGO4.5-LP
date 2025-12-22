import SPARQLWrapper

YAGO_ENDPOINT = "https://yago-knowledge.org/sparql/query"

def get_yago_endpoint() -> SPARQLWrapper.SPARQLWrapper:
    """
        Create and return a SPARQLWrapper endpoint configured for the YAGO knowledge graph.

        The returned endpoint is preconfigured with:
        - the YAGO public SPARQL endpoint URL
        - JSON as the return format

        A new SPARQLWrapper instance is created on each call, making this function
        safe to use in multithreaded contexts (the endpoint object is not shared
        across threads).

        :return: A configured SPARQLWrapper instance ready for queries
        :rtype: SPARQLWrapper.SPARQLWrapper
    """
    yago_endpoint = SPARQLWrapper.SPARQLWrapper(
        "https://yago-knowledge.org/sparql/query"
    )
    yago_endpoint.setReturnFormat(SPARQLWrapper.JSON)
    return yago_endpoint
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


def compute_node_degree(node_uri: str) -> int:
    """
        Compute the total degree of a node in the YAGO knowledge graph.

        This function counts both outgoing and incoming edges of the given node URI.
        Outgoing edges are triples where the node is the subject, and incoming edges
        are triples where the node is the object. Only edges pointing to or coming
        from other URIs are counted.

        A new SPARQLWrapper endpoint is created for each call, making this function
        safe to use in multithreaded contexts.

        :param node_uri: The URI of the node whose degree is to be computed.
        :type node_uri: str
        :return: The total degree of the node (number of incoming + outgoing edges).
        :rtype: int
        :raises SPARQLWrapper.SPARQLExceptions: If there is an error executing the SPARQL queries.
    """
    endpoint = get_yago_endpoint()

    degree = 0

    # Outgoing edges
    endpoint.setQuery(f"""
        SELECT DISTINCT ?p ?o
        WHERE {{
            <{node_uri}> ?p ?o .
            FILTER(ISURI(?o)) .
        }}
    """)
    results = endpoint.queryAndConvert()
    degree += len(results["results"]["bindings"])

    # Incoming edges
    endpoint.setQuery(f"""
        SELECT DISTINCT ?s ?p
        WHERE {{
            ?s ?p <{node_uri}> .
        }}
    """)
    results = endpoint.queryAndConvert()
    degree += len(results["results"]["bindings"])

    return degree
import argparse
import csv

import SPARQLWrapper
import tqdm

from utils.logging_utils import get_logger


def main():
    parser = argparse.ArgumentParser(prog="get_shapes_info", description="Get shapes and number of target nodes")
    parser.add_argument("--output", dest="output", help="Output file", required=True)
    parser.add_argument("-l,--log-level", dest="log_level", help="Set the logging level", type=str,
                        default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    args = parser.parse_args()

    logger = get_logger(args.log_level)

    logger.info("get_shapes_info: start")
    logger.info(f"SPARQL endpoint: https://yago-knowledge.org/sparql/query")
    logger.info(f"Output file: {args.output}")

    yago_endpoint = SPARQLWrapper.SPARQLWrapper(
        "https://yago-knowledge.org/sparql/query"
    )
    yago_endpoint.setReturnFormat(SPARQLWrapper.JSON)

    shapes = []

    try:
        yago_endpoint.setQuery("""
            SELECT ?shape
            WHERE
            {
                ?shape rdf:type <http://www.w3.org/ns/shacl#NodeShape> .
            }
            """)

        results = yago_endpoint.queryAndConvert()

        for r in results["results"]["bindings"]:
            shapes.append([r["shape"]["value"], 0])

        logger.info(f"Number of shapes: {len(shapes)}")

        for s in tqdm.tqdm(shapes):
            yago_endpoint.setQuery(f"""
                SELECT (COUNT(*) AS ?targetNodes) 
                WHERE
                {{
                    ?s rdf:type/rdfs:subClassOf* <{s[0]}> .
                }}
            """)

            results = yago_endpoint.queryAndConvert()
            s[1] = results["results"]["bindings"][0]["targetNodes"]["value"]

    except Exception as e:
        print(e)

    with open(args.output, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(["Shape", "# target nodes"])
        csvwriter.writerows(shapes)

    logger.info("get_shapes_info: done")


if __name__ == '__main__':
    main()

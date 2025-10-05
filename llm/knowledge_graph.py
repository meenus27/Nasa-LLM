from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

def add_publication(metadata):
    with driver.session() as session:
        session.run("""
            MERGE (p:Publication {id: $id})
            SET p.title = $title, p.date = $date
        """, metadata)

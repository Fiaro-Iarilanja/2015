MATCH (n)
DETACH DELETE n;

UNWIND range(0, 19) AS id
CREATE (:cNode {id: id});

UNWIND range(0, 19) AS id
CREATE (:Node {id: id});

UNWIND range(1, 19) AS i
WITH i, toInteger(rand() * i) AS j
MATCH (a:cNode {id: i})
OPTIONAL MATCH (b:cNode {id: j})
CREATE (a)-[:TO]->(b);

UNWIND range(1, 19) AS x
WITH
  toInteger(rand() * 20) AS a,
  toInteger(rand() * 20) AS b,
  rand() AS probability
WHERE a <> b AND probability >= 0.5
MATCH (n1:Node {id: a})
OPTIONAL MATCH (n2:Node {id: b})
MERGE (n1)-[:TO]->(n2);

MATCH (n:Node)
WHERE NOT EXISTS((n)-[]->()) OR NOT EXISTS(()-[]->(n))
WITH COLLECT(n) AS sources
UNWIND sources AS source
WITH toInteger(rand() * 20) AS targetId, source
MATCH (n2:cNode {id: targetId})
MERGE (source)-[:TO]->(n2)
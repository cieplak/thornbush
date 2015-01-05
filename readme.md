# Thornbush

Thornbush is a simple REST API for threaded comments.

## Examples

Create a comment:

    curl localhost:8000/comments -U root:secret_5GHu1EDmw2n4P3o9dMaBZC \
      -H "Content-Type: application/json" \
      -X POST \
      -d '{"text": "XML has better schema validation capabilities."}'

    {
      "id": "Cguknefh274",
      "created_at": "2014-01-01",
      "updated_at": "2014-01-01",
      "version": 0,
      "user": "root",
      "text": "XML has better schema validation capabilities."
      "parent": null,
      "children": []
    }
    
Comment on a comment:

    curl localhost:8000/comments/Cguknefh274/comments \
      -U root:secret_5GHu1EDmw2n4P3o9dMaBZC \
      -H "Content-Type: application/json" \
      -X POST \
      -d '{"text": "Yes but it makes my eyes bleed"}'

    curl localhost:8000/comments/ \
      -U root:secret_5GHu1EDmw2n4P3o9dMaBZC \
      -H "Content-Type: application/json" \
      -X POST \
      -d '{"parent": "Cguknefh274", \
           "text": "Yes but it makes my eyes bleed"}'

Fetch a comment (default depth is 0):

    curl localhost:8000/comments/Cguknefh274 -U root:secret_5GHu1EDmw2n4P3o9dMaBZC 

Fetch a comment and n generations:

    curl localhost:8000/comments/Cguknefh274?depth=$n \
      -U root:secret_5GHu1EDmw2n4P3o9dMaBZC \
      -H "Content-Type: application/json"

Fetch a comment and all its descendants (set -1 as depth):

    curl localhost:8000/comments/Cguknefh274?depth=-1 -U root:secret_5GHu1EDmw2n4P3o9dMaBZC 

Fetch the first version of a comment:

    curl localhost:8000/comments/Cguknefh274?version=0 -U root:secret_5GHu1EDmw2n4P3o9dMaBZC 

Fetch the comment index (default page size is 100 comments):

    curl localhost:8000/comments -U root:secret_5GHu1EDmw2n4P3o9dMaBZC 

Search the comments for keywords(default page size is 100 comments):

    curl localhost:8000/comments?contains=keyword,keyword2 \
      -U root:secret_5GHu1EDmw2n4P3o9dMaBZC 

View a users comments:

    curl localhost:8000/users/root/comments -U root:secret_5GHu1EDmw2n4P3o9dMaBZC 
      
    curl localhost:8000/comments?user=root -U root:secret_5GHu1EDmw2n4P3o9dMaBZC 

Search a user's comments for keywords:

    curl localhost:8000/users/root/comments?contains=keyword,keyword2 \
      -U root:secret_5GHu1EDmw2n4P3o9dMaBZC 

Edit a comment (note that version is incremented):

    curl localhost:8000/comments/Cguknefh274 \
      -U root:secret_5GHu1EDmw2n4P3o9dMaBZC \
      -H "Content-Type: application/json" \
      -X PUT \
      -d '{"comment": "XML has better schema validation capabilities."}'

    {
      "id": "Cguknefh274",
      "created_at": "2014-01-01",
      "updated_at": "2014-01-01",
      "version": 1,
      "user": "root",
      "text": "XML has better schema validation capabilities."
      "parent": null,
      "children": []
    }      

Delete a comment:

    curl localhost:8000/comments/Cguknefh274 -X DELETE
      
    {
      "id": "Cguknefh274",
      "deleted_at": "2014-12-25 01:17:58.769854"
    }

Idempotently create a comment (specify GUID client side):

    curl localhost:8000/comments/Cguknefh274 \
      -H "Content-Type: application/json" \
      -X PUT \
      -d '{"text": "XML has better schema validation capabilities."}'

    {
      "id": "Cguknefh274",
      "text": "XML has better schema validation capabilities."
      "parent": null,
      "children": []
    }   

Create a user:

    curl localhost:8000/users \
      -H "Content-Type: application/json" \
      -X POST \
      -d '{"name": "cieplak"}'
      
    {
      "name": "cieplak",
      "key": "secret_123123"
    }

Delete a user:

    curl localhost:8000/comments/Cguknefh274 -X DELETE

    {
      "id": "Cguknefh274",
      "deleted_at": "2014-01-01"
    }

## Getting set up

Install Postgres and ElasticSearch then run 

    python setup.py install

    bin/thornbush api

## Running the tests

    tox

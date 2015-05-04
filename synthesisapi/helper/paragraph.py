# File containing helper functions dealing
# With paragraph and query objects
from bson import ObjectId

''' Adds paragraphs to given query-paragraph pair
    Input:
        connection      mongodb connection
                        required: have registered Paragraph, Query
    
        data            [(material_id, paragraph, rank)...]                             
                        paragraph = {...}
    Output:
'''
def add_paragraphs(connection,data):
    pa_collection = connection['synthesis-api'].paragraphs
    qy_collection = connection['synthesis-api'].queries

    # TODO: do we need a try/catch?
    for (material_id, paragraph, rank) in data:
        # Creating a paragraph object if it does not exist
        paragraph_object = pa_collection.Paragraph.find_and_modify(
            {'doi': paragraph['doi'], 'text': paragraph['text']},
            update={'$setOnInsert': { 
                            'feature_vector': paragraph['feature_vector'],
                            'is_recipe': paragraph['is_recipe'],
                            'doi': paragraph['doi'], 
                            'text': paragraph['text'] }
            },
            upsert=True,
            new=True)
         
        # Incudes paragraph into query
        query = qy_collection.Query.find_and_modify(
            {'material_id': material_id, 'paragraph': paragraph_object['_id']},
            update={
                'material_id': material_id,
                'rank': rank,
                'paragraph': paragraph_object['_id']
            },
            upsert=True,
            new=True)


''' Removes paragraphs for the given query-paragraph pairs
    Input:
        connection      mongodb connection
                        required: have registered Paragraph, Query
    
        data            [(material_id, paragraph)...]                             
                        paragraph = {...}
    Output:
'''
def remove_paragraphs(connection,data):
    pa_collection = connection['synthesis-api'].paragraphs
    qy_collection = connection['synthesis-api'].queries

    # TODO: do we need a try/catch?
    for (material_id, paragraph, rank) in data:
        # Finds the paragraph object
        paragraph_object = pa_collection.Paragraph.find_one(
            {'doi': paragraph['doi'], 'text': paragraph['text']})
        
        if paragraph_object is not None:
            # Removes paragraph object from query  
            query = qy_collection.remove(
                {'material_id': material_id, 'paragraph': paragraph_object['_id']})


''' Gets a list of paragraphs ids related to the query
    Input: 
        connection      mongodb connection
                        required: have registered Paragraph, Query
    
        material_id     id of the given material requested data from

    Returns:
        Cursor to the list of ids

'''
def get_paragraph_ids_of_query(connection, material_id, amt):
    qy_collection = connection['synthesis-api'].queries
    # Currently just returns 5, not ranked. Sort later when rank means something
    return qy_collection.Query.find({'material_id': material_id}, {'_id': False}, limit=amt)


''' Gets a list of paragraphs related to the query
    Input: 
        connection      mongodb connection
                        required: have registered Paragraph, Query
    
        material_id     id of the given material requested data from

    Returns:
        Cursor to the list of paragraph objects

'''
def get_paragraphs_of_query(connection, material_id, amt):
    pa_collection = connection['synthesis-api'].paragraphs
    ids = list(get_paragraph_ids_of_query(connection, material_id, amt).limit(amt))
    
    paragraph_query = [{'_id': item['paragraph']} for item in ids]

    return pa_collection.find({"$or": paragraph_query}, {'_id': False})

''' Validates if the paragraph-query given is a valid pair
    Input:

    Returns:
        True if it is a valid pair, false otherwise
'''
def validate_paragraph_query(connection, paragraph_id, material_id):
    qy_collection = connection['synthesis-api'].queries
    doc = qy_collection.Query.find_one({'material_id': material_id, 'paragraph': paragraph_id})
    return (doc is not None)

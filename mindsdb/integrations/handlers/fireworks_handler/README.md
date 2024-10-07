---
title: Fireworks
sidebarTitle: Fireworks
---

This documentation describes the integration of MindsDB with [Fireworks](https://fireworks.ai/), production AI platform
built for developers. Fireworks partners with the world's leading generative AI researchers to serve the best models, at the fastest speeds.

## Prerequisites

Before proceeding, ensure the following prerequisites are met:

1. Install MindsDB [locally via Docker](https://docs.mindsdb.com/setup/self-hosted/docker) or [Docker Desktop](https://docs.mindsdb.com/setup/self-hosted/docker-desktop).
2. To use Fireworks within MindsDB, install the required dependencies following [this instruction](/setup/self-hosted/docker#install-dependencies).
3. Obtain the Fireworks API key required to deploy and use Fireworks llms within MindsDB. Follow the [instructions for obtaining the API key](https://readme.fireworks.ai/docs/quickstart).

## Setup

Create an AI engine from the [Fireworks handler](https://github.com/mindsdb/mindsdb/tree/staging/mindsdb/integrations/handlers/fireworks_handler).

```sql
CREATE ML_ENGINE fireworks_engine
FROM fireworks
USING
    fireworks_api_key = 'your-fireworks-api-key';
```

Create a text query model using `fireworks_engine` as an engine.

```sql
CREATE MODEL fireworks_textmodel
PREDICT target_column
USING
      engine = 'fireworks_engine',  -- engine name as created via CREATE ML_ENGINE
      column = 'column_name',       -- column that stores input/question to the model
      max_tokens = <integer>,       -- max number of tokens to be generated by the model (default is 100)
      mode = 'conversational',      -- use mode as conversational
      model = 'model_name';         -- choose one of the available  text language models in fireworks-ai
```

Create a text vision model using `fireworks_engine` as an engine.

```sql
CREATE MODEL fireworks_visionmodel
PREDICT target_column
USING
      engine = 'fireworks_engine',  -- engine name as created via CREATE ML_ENGINE
      column = 'column_name',       -- column that stores image url link to the model
      mode = 'image',               -- use mode as image
      model = 'model_name';         -- choose one of the available vision language models in fireworks-ai
```

Create a text embedding model using `fireworks_engine` as an engine.

```sql
CREATE MODEL fireworks_embedding_model
PREDICT target_column
USING
      engine = 'fireworks_engine',  -- engine name as created via CREATE ML_ENGINE
      column = 'column_name',       -- column that stores input text 
      mode = 'embedding',           -- use mode as embedding
      model = 'model_name';         -- choose one of the available embedding language models in fireworks-ai
```


<Info>

The integrations between Fireworks and MindsDB was implemented using [Fireworks Python SDK](https://readme.fireworks.ai/docs/quickstart).
</Info>

## Usage

The following usage examples utilize `fireworks_engine` to create a model with the `CREATE MODEL` statement.

Create and deploy the Fireworks Text model within MindsDB to ask any question.

```sql
CREATE MODEL fireworks_text_model
PREDICT answer
USING
    engine = 'fireworks_engine',  
    column = 'question',       
    model = 'llama-v2-7b-chat',
    max_tokens = 200,
    mode = 'conversational';  

```

Where:

| Name              | Description                                                               |
|-------------------|---------------------------------------------------------------------------|
| `column`          | It defines the prompt to the model.                                       |
| `engine`          | It defines the Fireworks engine.                                          |
| `max_tokens`      | It defines the maximum number of tokens to generate before stopping.      |
| `model`           | It defines model that will complete your prompt.                          |
| `mode`            | It defines the mode type of the model                                     |


Create and deploy the Fireworks Vision model within MindsDB to ask any question.

```sql
CREATE MODEL fireworks_vision_model
PREDICT image_description 
USING
    engine = 'fireworks_engine',  
    column = 'image_url',       
    model = 'firellava-13b',
    mode = 'image';  

```

Where:

| Name              | Description                                                               |
|-------------------|---------------------------------------------------------------------------|
| `column`          | It defines the prompt to the model.                                       |
| `engine`          | It defines the Fireworks engine.                                          |    
| `model`           | It defines model that will complete your prompt.                          |
| `mode`            | It defines the mode type of the model                                     |



Create and deploy the Fireworks Embedding model within MindsDB to ask any question.

```sql
CREATE MODEL fireworks_embedding_model
PREDICT embeddings 
USING
    engine = 'fireworks_engine',  
    column = 'text',       
    model = 'nomic-ai/nomic-embed-text-v1.5',
    mode = 'embedding';  
```

Where:

| Name              | Description                                                               |
|-------------------|---------------------------------------------------------------------------|
| `column`          | It defines the prompt to the model.                                       |
| `engine`          | It defines the Fireworks engine.                                          |    
| `model`           | It defines model that will complete your prompt.                          |
| `mode`            | It defines the mode type  of the model                                    |




<Info>

**Default Max Tokens**

When you create an Fireworks model in MindsDB with `QueryTextModel` as task then it uses 100 tokens as the maximum by default. But you can adjust this value by passing it to the `max_tokens` parameter in the `USING` clause of the `CREATE MODEL` statement.
</Info>

Query the Text model to get predictions.

```sql
SELECT question, answer
FROM fireworks_text_model
WHERE question = 'Where is Stockholm located?';
```

Here is the output:

```sql
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| question                    | answer                                                                                                                                             |
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| Where is Stockholm located? | Thank you for asking! Stockholm is located in Sweden, Europe. It is situated on the coast of the Baltic Sea and is the capital and largest city of Sweden. Stockholm is known for its rich history, cultural heritage, and architectural landmarks, including the Vasa Museum, the Royal Palace, and the Old Town (Gamla Stan). It is also a hub for Swedish design, fashion, and cuisine, and offers a vibrant cultural scene with many museums, galleries, and festivals throughout the year. Is there anything else I can help you with?  |
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
```

Query the vision model to get predictions.

```sql
SELECT image_url, image_description 
FROM fireworks_vision_model
WHERE image_url = 'https://images.unsplash.com/photo-1582538885592-e70a5d7ab3d3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1770&q=80';
```

Here is the output:

```sql
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| image_url                    | image_description                                                                                                                                             |
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| https://images.unsplash.com/photo-1582538885592-e70a5d7ab3d3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1770&q=80 |  In the image, a large group of blurry cherry trees surrounds a tower in the background. The trees are in bloom, displaying vibrant pink flowers that contrast with the blue sky above. The foreground of the image features vibrant pink flowers arranged in a clump, creating a visually appealing pattern. The overall scene suggests that spring has arrived, and the cherry trees are in full bloom, creating a picturesque landscape. |
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
```


Query the Embedding model to get predictions.

```sql
SELECT text, embeddings
FROM fireworks_embedding_model
WHERE text = 'Where is Stockholm located?';
```

Here is the output:

```sql
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| text                    | embeddings                                                                                                                                            |
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| Where is Stockholm located? | [0.013214111328125,0.029541015625,-0.1593017578125,-0.032806396484375,-0.046722412109375,0.031982421875,0.0086669921875,........,-0.00925445556640625,0.032257080078125,0.05780029296875,-0.07391357421875,0.0031681060791015625,-0.0228424072265625,-0.0000095367431640625]
1 to 1 of 1  |
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
```
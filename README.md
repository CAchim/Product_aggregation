<h1> P3 - Produse </h1><br>
<h2> Product aggregation project</h2>

Team members: <br>
<ol>
  <li>Achim Catalin</li>
  <li>Dimcea Alexandra</li>
  <li>Petrasca Nicoleta</li>
</ol> 

Project Steps:<br>

<h2>#O1</h2><br>
For this objective the following python packages needs to be installed. NOTE! If pip3 does not work, use just pip:<br>
 <ul>
  <li>extruct -> pip3 install extruct</li>
  <li>requests -> pip3 install requests</li>
  <li>w3lib -> pip3 install w3lib</li>
</ul> 

Description: <br>
<ol>
  <li>Implements the DataExtraction class that can be found in DataExtraction.py</li>
  <li>DataExtraction class is used to extract the metadata from a website (shopping website) and with it we can extract the info about products drom that websites. The metadata contains the Schema.org info about that          specific product and after the class extracts it, the class also parse that metadata and find the information       about that prduct ( name, price, reviews and so on)</li>
  <li>DataExtraction class is initialized with a list of URLs to different products from websites, and after it    extracts the info about each product it returns a list of Product objects. the Product class defines how a            product should look like. This way it will be easier to parse the products at the end</li>
  <li>In the main.py an example of how the DataExtraction class work is demonstrated and explained</li>
</ol> 

Workflow<br><br>
```mermaid
graph LR;
    URLS-->DataExtractionClass;
    subgraph A[" "]
    DataExtractionClass-->|handling|id1(raise exception if url is bad);
    end
    DataExtractionClass-->|run|id2(get_products_info function);    
    id2-->|returns|id3(list of Product objects);
```

<h2>#O2</h2><br>
For this objective the following python packages needs to be installed. NOTE! If pip3 does not work, use just pip:<br>
 <ul>
  <li>rdflib -> pip3 install rdflib</li>
</ul> 

Description: <br>
<ol>
  <li>This step implements the PersistenceDB class that is found in the Persistence.py file</li>
  <li>The PersistenceDB class converts the Product objects to the previus step in RDF and stores them in a ttl
  (turtle) file which acts like a small database stored on the disk</li>
  <li>The class appends new products to the database file and keeps the old data, this way we have access to
  the old data as well and the database role it's mantained</li>
</ol> 

<h2>#O3</h2><br>
Description: <br>
<ol>
  <li>This steps also uses the PersistenceDB class.</li>
  <li>Loads the ttl file in momory and from there it runs SPARQL querys in order to get the desired info about a  product</li>
  <li>The class implements a few methods that retrieve the data and alto it has the capability to add some filtering based on the user choiche</li>
</ol> 

Bibliography: <br>
<ol>
  <li>rdflib - https://rdflib.readthedocs.io/en/stable/</li>
  <li>extruct - https://github.com/scrapinghub/extruct</li>
  <li>w3lib - https://w3lib.readthedocs.io/en/latest/</li>
</ol>
      

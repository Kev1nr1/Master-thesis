In dit bestand wordt kort uitgelegd wat de functie is van alle bestanden:


Ipynb files:
-data_exploration.ipynb
	cleaned vulnerability dataset wordt initieel geanalyseerd
-First_API_call_extraction.ipynb
	de initiele API call resultaten worden omgezet naar bruikbare data: dit wordt apart gedaan om geen problemen te creeeren in het process zodat de API call kan blijven runnen
	dit levert uiteindelijk de resultaten voor de lijst met 5 categorieen per product
-individual LDA.ipynb
	De gevonden categorieen kunnen hierin topic modeling gedaan worden: dit is handmatig gedaan aangezien de tijd het niet toeliet om alle categorieen te runnen voor topic modelling
	Hierin worden alle parameters eerst gerunned voor een optimaal model voor de LDA
-individual LDA_IoT.ipynb
	Zelfde als hier boven: dan alleen voor de dataset van het IoT lab
-Initial data creation.ipynb
	De initiele data die gepulled is van de EUVD wordt hier gecleaned en voorbereid voor vervolg stappen
-kruskal wallis.ipynb
	Statistische analyse wordt hierin berekend en ge explored
-kruskal wallis_IoT.ipynb
	Zelfde als hierboven, voor IoT dataset
-LDA_best_model.ipynb
	Werd initieel gebruikt: globaal model gemaakt om tussen de topics te kunnen vergelijken met Jensen-Shannon distance:
	Levert bias op, dus niet toegepast. Misschien nuttig, maar waarschijnlijk kan dit genegeerd worden
-LDA_best_model_IoT.ipynb 
	Zelfde weer, voor IoT lab
-mistral call.ipynb
	De API call werd hierin gedaan: key en link weggehaald, moet weer toegevoegd worden als bruikbaar
	Geen automatische functie in Azure voor caching: daarom poging gedaan met content van system zelfde tegenover nieuwe content op de user role (dit zou kunnen werken, heb niet kunnen verifieren of dit minder tokens verbruikt)
	In batches van 10 gevraagd
	De eerste call zorgt voor de initiele 5 categorieen per product
	De tweede call is voor het classificieren in de gevonden categorien
	De derde call is zelfde als tweede maar dan met product categorieen van IoT lab
	Wordt opgeslagen in een .txt bestand zodat dit raw is 
	Wel gevraagd aan AI om dit in JSON te formuleren maar aangezien dit fouten kan maken wordt dit pas later ge extract
-Pulling data API.ipynb
	Hierin wordt de initiele data van de EUVD gepulled
	Hierin moet de parameters dan wel aangepast worden aangezien dit een crash save is: (opgepakt nadat het ergens gestopt was met runnen)
-Second_API_call_extraction
	Zelfde als eerste maar dan voor AI categorieen
-Third_API_call_extraction.ipynb
	Zelfde als eerste maar dan voor IoT categorieen

Python file:
-html converter.py
	Zorgt er voor dat de LDA topic modelling omgezet wordt naar een mooie visualisatie (gevibecoded naar een design die ik gemaakt heb in photoshop)
	Gebruik hiervoor de lda_topics_all.txt en lda_topics_all_IoT.txt
	Optimaal dit natuurlijk automatiseren met de LDA topic analysis


HTML files:
	Dit zijn de output files van de html converter
	Gewoon een front end design voor de LDA topic modelling


CSV files:
-5 categories.csv
	De initiele gevonden categorieen van de producten van de AI call
-category_changes.csv
	Automatisering handmatig werk: is gecontroleerd, scheelt veel tijd, niet relevant meer
-classification.csv
	Zelfde als hier boven
-cleaned_vulnerabilities.csv
	De initiele dataset die gecleaned is waarbij niet relevante CVE er uit gehaald zijn en voorbereid zijn voor tekst analyse op de description
-labeled_vulnerabilities.csv
	Belangrijke dataset: hierin zijn alle producten gelabelled aan een product categorie van de AI
-labeled_vulnerabilities_IoT.csv
	Zelfde als hier boven maar dan voor IoT categorieen
-product_vendor_combinations.csv
	Gepulled van de originele dataset, dit werd meegegeven aan AI calls om op te zoeken, is gefiltered op duplicates enz
-vulnerabilities_10_years.csv
	De originele dataset die gebruikt is voor dit onderzoek waar nog niks mee gedaan is


Txt files:
-array_vertical.txt
	AI categorieen
-array_vertical_IoT.txt
	IoT categorieen
-failed_blocks.txt
	Gefaalde blocks voor extraction 1
-failed_blocks_2.txt
	Gefaalde blocks voor extraction 2
-failed_blocks_3.txt
	Gefaalde blocks voor extraction 3



Als er vragen zijn over code/keuzes, mail mij gerust naar k.w.rijnders@students.uu.nl of als dit niet meer in gebruik is naar kevinwesleyrijnders@gmail.com

	

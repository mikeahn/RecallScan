# RecallScan

Ever bought a grocery, only to find out it was recalled for scary reasons? Simply scan the barcode, RecallScan will tell you if it was recalled within the last 2 years. Stay safe & proactive!

## Inspiration
UPC barcodes are standardized global identifiers, which enable products to be sold, reordered and tracked through supply chains.  Accurate product identification starts with the UPC barcode since it is the key to which everything is based on. To provide better service in alerting the American people to unsafe, hazardous or defective products, six federal agencies with vastly different jurisdictions have joined together to create www.recalls.gov -- a "one-stop-shop" for U.S. Government recalls.
However, it is neither well known nor readily-accessible to the general population and it is particularly tedious to keep up-to-date information about _recalled food products_. Compared to other recalled product categories such as vehicles and medicine, food products require more careful attention from the general population especially because of its variety, accessibility, and a relatively cheap price range. 

## What it does
We present a novel mobile app that allows users to easily and quickly check the safety of food products during grocery shopping. Simply by overlaying a camera lens provided by the app onto the _barcode_ of the desired food product, RecallScan app scans the barcode, matches with the up-to-date recall database, and provides information about its safety status and its details in real-time. Such information is directly provided from the website(www.recalls.gov), which is the first place such information becomes available to the public.

## How we built it
Configured Apache and SSL connection on the cloud webserver  
Authored python BeautifulSoup script that crawls FDA and Consumer Product Safety Commission's recall alert webpage to collect product information and download images  
Imported crawled data to a web server database and deployed Flask web app to serve as API endpoint to our application  
Designed an effective API structure for efficient frontend/backend data exchange  
Added a layer of automation on the webserver to regularly crawl for new data and minimize manual data management  

From the web-extracted image of recalled products separated the image into Scharr gradient in both x and y directions  
Removed horizontal gradient information to target vertical barcode formats  
Isolated barcode region by blurring unnecessary information and binary thresholding  
Performed morphological operations(erosion and dilation) using a rectangular structuring element  
Identified largest components to capture the barcode region and read the barcode  
Saved extracted UPC from barcode into SQL DB  

Developed a fully functioning iOS application using Swift and Xcode  
Implemented barcode scanning feature using Apple’s AVFoundation framework  
Implemented API request and JSON parsing functions to fetch corresponding data for each scanned items  
Created popup screens to see necessary data, mainly to notify whether items had defects in the past  
Touched on aesthetics on the client side interface for better user experiences    

While working on each person's specialties, continuously shared feedback on each other's implementations  

## Challenges we ran into
Currently, the government-provided recall information is semi-structured and they often do not provide the UPC barcode information. Because having the correct UPC information of the recalled food products in our database is critical to the accuracy and efficiency of RecallScan, we utilized geometric computing methods to extract and identify UPC barcodes from the provided images of recalled food products. However, because the provided images were sourced from firsthand press-released photos, they vary tremendously in terms of image quality, scale, and orientation. It was challenging to build a complete database of recalled food products because often, UPC wasn't provided and the product images weren't informative enough to uniquely identify and codify the product.

## Accomplishments that we're proud of
RecallScan provides a first-ever proactive platform for the users to identify and avoid potentially harmful food products, replacing the current way of manually checking the government website for the latest posts about recalled food products. Also, users can get real-time answers with minimal intervention from their end, making it extremely usable and effective.

## What we learned
The project was an application of the skills and knowledge we gained from the classroom and through work/research experiences. Developing a project from scratch in 2 days was a very challenging experience, particularly because it was the first hackathon for all of our team members. We had to weigh out the potential times that would be spent for each component of the project and even boldly drop or add ideas flexibly as we went. As a group of prospective engineers ourselves, it was a unique experience to gather very different expertise from each of our members and put all of our effort to develop a product that would benefit the most under such time and physical constraints. We are passionate about our project and we were amazed to see each component come together, in the end, to produce something meaningful for the world, and not a mere energy-consuming data dump in the modern digital world.

## What's next for RecallScan
We are aiming to expand RecallScan in various ways. First, alongside with the mobile app to look up individual items in-hand, we plan to provide a comprehensive recalled products information board on our web domain for easy look-up. Moreover, we want to provide recall information not only with the barcode reading service but also provide the same information by capturing the front image of the product even when the barcode information is not extractable.

Also, we will add multithreading to the crawler script so that new information can be added to our database more efficiently. Ultimately the database we gathered will be offered on our website as well so that recallScan can be a go-to place for any recall-related issues. 

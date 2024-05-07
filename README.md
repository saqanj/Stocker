# Stocker: An AI-Generated Stock Blog (Version: 2.0.0, 05/07/2024)

# Application Overview
- If you are accessing this for the first time, please navigate to the original repository's README for further context before proceeding here. Here is a link: [PREVIOUS README LINK](https://github.com/KwadwoAK/ChatAPI/blob/main/README.md#stocker-an-ai-generated-stock-blog).
- In this new version of Stocker, we are using Ollama and MySQL on a local cluster spun up using a Helm-Chart. Also, we have three synchronously running microservices: AIClientMicroservice, FrontEndMicroservice, and DBMicroservice. The only thing that is missing is the GatewayAPI for the reasons stated in the original repository. Essentially, the application overview is mostly the same as before except Ollama is on the cluster and is no longer an external OpenAI API. All of the microservices are port-forwarded on the cluster, and interaction must be done directly as opposed to through an interactive Gateway Interface. We make use of Postman Collection during our presentation of this material. The FrontEndMicroservice is also a brand-new microservice that was used in place of Ghost on the local cluster, using a basic static.html from Flask for the Blog Posts. A step-by-step outline will be provided.

# Collaboraters
- Saqlain Anjum, sanjum@trincoll.edu
- Kwadwo Osarfo-Akoto, kosarfoa@trincoll.edu
- Joachim Chuah, jchuah@trincoll.edu 

# UML
![Project UML](https://github.com/saqanj/Stocker/assets/134897920/6e317f50-3b64-410b-8fbf-49d9fcaf55b6)

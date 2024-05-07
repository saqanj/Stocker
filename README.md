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

# Languages and Frameworks
- Spring/SpringAI
- Java
- Docker
- Kubernetes
- MySQL
- Python
- Helm 
- REST
- JSON Data Format
- Postman

# Modules
- Database Microservice
- AI Client Microservice
- Front-End Microservice

# Sources
- Here is a list of all open-source resources utilized to make Stocker possible:
  - [Ghost Helm](https://artifacthub.io/packages/helm/bitnami/ghost)
  - [MySQL Helm](https://artifacthub.io/packages/helm/bitnami/mysql)
  - [SpringAI Docs for OpenAI](https://docs.spring.io/spring-ai/reference/api/clients/openai-chat.html)
  - [YahooFinance Data Collection](https://github.com/TheMultivariateAnalyst/Finance_Database_SQL)
 
 # UI Description + Primary Actions
- A simple static.html page in the Front End Microservice is the project's front-end. The blog post is updated using Post from Postman with the blog-post generated from previous rest calls.

# Executing the Application 
- In order to proceed with this, ensure that you have at least 16GB Ram on your local machine. This project was tested using a Macbook Pro with an Apple Silicon M1 Chip and 16GB Ram. Another machine of similar or more specs would be required. On your local kubernetes cluster, create the following namspaces:
```
kubectl create namespace stk-helm-mysql
```
```
kubectl create namespace stk-aimicroservice
```
```
kubectl create namespace stk-dbmicroservice
```
```
kubectl create namespace stk-frontendmicroservice
```
```
kubectl create namespace stk-helm-ollama
```
- Ensure the following for using a helm-chart on your machine:
```
brew install helm
```
- Or for Linux:
```
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```
- Once Helm is installed, to install the MySQL pod on Kubernetes using Helm follow these commands in the kubernetes directory of this repository:
```
helm repo add bitnami https://charts.bitnami.com/bitnami
```
```
helm install my-mysql bitnami/mysql \
  --version 10.1.1 \
  --namespace stk-helm-mysql \
  --create-namespace \
  --values mysql-values.yaml
```
- Once you have MySQL installed, use the following commands to get access to the MySQL Database.
- To get the password (it should be `mypassword` but it is worth checking):
```
echo $MYSQL_ROOT_PASSWORD
```
- Then run this command to get it started:
```
kubectl run my-mysql-client --rm --tty -i --restart='Never' --image  docker.io/bitnami/mysql:8.0.36-debian-12-r10 --namespace (PREVIOUSLY USED NAMESPACE) --env MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD --command -- bash
```
- Run the following commands sequentially for spinning up Ollama using helm:
```
helm repo add ollama-helm https://otwld.github.io/ollama-helm/
```
```
helm repo update
```
```
helm install ollama ollama-helm/ollama --namespace stk-helm-ollama --values ollama-values.yaml
```
- Once more, ensure you are in the kubernetes directory of this repository as instructed above. Now that each helm-initiated pod is spun up, we must apply the necessary files on kubernetes to have everything running:
```
kubectl apply -f aiclient-deployment.yaml -f aiclient-service.yaml -f aiclient-configmap.yaml -n stk-aimicroservice
```
```
kubectl apply -f db-deployment.yaml -f db-service.yaml -f db-configmap.yaml -n stk-dbmicroservice
```
```
kubectl apply -f poster-deployment.yaml -f poster-service.yaml -n stk-postermicroservice
```
- You must also port-forward each microservice like so:
```
kubectl port-forward -n stk-aimicroservice service/aiclient-service 8080:8080
```
```
kubectl port-forward -n stk-dbmicroservice service/stock-app-service 5000:5000
```
```
kubectl port-forward -n stk-postermicroservice service/frontend-service 5010:5010
```
- Once each microservice is port-forwarded, you can use the IP address listed upon port-forwarding to access different routes directly on your browser, or use Postman Collections. The routes accessed are indicated in the following links sequentially:
    1. http://127.0.0.1:5000/start_fetching - This route will initiate the stock-data fetching process.
    2. http://127.0.0.1:5000/all_stock_data - This will display the fetched stock-data in JSON format. You must store this, or have this displayed in your Postman Collection.
    3. http://127.0.0.1:8080/ai/generate/beginConversation - This route begins the conversation with Mistral.
    4. http://127.0.0.1:8080/ai/generate/introduceAssignment - This route lets Mistral know what it must do for the Blog Post.
    5. http://127.0.0.1:8080/ai/generate/updateData - You can provide the stored Stock data as a parameter to this route on your Postman Collection.
    6. http://127.0.0.1:8080/ai/generate/firstPrompt - This route will generate the first-prompt and provide the AI Analysis that needs to be sent to the Blog-Post Front-End.
    7. http://127.0.0.1:5010/postdata - You can provide the AI output from the previous route to this route as a parameter for the front-end to be displayed.
    8. http://127.0.0.1:5010/ - You can use this to then view your Stock UI Static HTML page with the new Blog Post.
    9. Repeat step 1, 2, 5, and run this route for a new AI Post to be generated: http://127.0.0.1:8080/ai/generate/subsequentPrompts
    10. You can then use step 7 and 8 to view updated blog posts.
 
# Lessons Learned & Project Recap
- 

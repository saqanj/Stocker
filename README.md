# Stocker: An AI-Generated Stock Blog (Version: 2.0.0, 05/07/2024)

# Application Overview
- If you are accessing this for the first time, please navigate to the original repository's README for further context before proceeding here. Here is a link: [PREVIOUS README LINK](https://github.com/KwadwoAK/ChatAPI/blob/main/README.md#stocker-an-ai-generated-stock-blog).
- In this new version of Stocker, we are using Ollama and MySQL on a local cluster spun up using a Helm-Chart. Also, we have three synchronously running microservices: AIClientMicroservice, FrontEndMicroservice, and DBMicroservice. The only thing that is missing is the GatewayAPI for the reasons stated in the original repository. Essentially, the application overview is mostly the same as before except Ollama is on the cluster and is no longer an external OpenAI API. All of the microservices are port-forwarded on the cluster, and interaction must be done directly via Postman as opposed to through an interactive Gateway Interface. We make use of Postman Collection during our presentation of this material. The FrontEndMicroservice is also a brand-new microservice that was used in place of Ghost on the local cluster, using a basic static.html from Flask for the Blog Posts. A step-by-step outline will be provided. For additional information on each individual microservice, please navigate to the original README above. The communication is all the same except it is using Postman for communication and Ollama spun up locally on Mistral as the AI Model.

# Collaboraters
- Saqlain Anjum, sanjum@trincoll.edu
- Kwadwo Osarfo-Akoto, kosarfoa@trincoll.edu
- Joachim Chuah, jchuah@trincoll.edu 

# Component Diagram
![Project UML](https://github.com/saqanj/Stocker/assets/134897920/6e317f50-3b64-410b-8fbf-49d9fcaf55b6)

# Languages and Frameworks
- Spring/SpringAI
- Java
- Docker
- Kubernetes
- MySQL
- Python
- Flask
- YahooFinance Python Library
- Helm 
- REST
- JSON Data Format
- Postman
- Ollama

# Modules
- Database Microservice
- AI Client Microservice
- Front-End Microservice

# Sources
- Here is a list of all open-source resources utilized to make Stocker possible:
  - [MySQL Helm](https://artifacthub.io/packages/helm/bitnami/mysql)
  - [Ollama Helm](https://artifacthub.io/packages/helm/ollama-helm/ollama?modal=values)
  - [SpringAI Docs for OpenAI](https://docs.spring.io/spring-ai/reference/api/clients/openai-chat.html)
  - [YahooFinance Data Collection](https://github.com/TheMultivariateAnalyst/Finance_Database_SQL)
  - [Postman Docs](https://learning.postman.com/docs/introduction/overview/)

 
 # Features / Minimum Viable Product Goals
- A simple static.html page in the Front End Microservice is the project's display of a minimum viable product successfully functioning. If execution directions are followed, the application should support the creation of a simple AI-Generated Stock Blog-Post on this HTML Front-End that you should be able to access in your browser!

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
- Ensure the following for using a helm-chart on your machine if you have MacOS and brew installed:
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
- Type "exit" to get out of the MySQL pod you just spun up on Kubernetes. Now, run the following commands sequentially for spinning up Ollama using helm:
```
helm repo add ollama-helm https://otwld.github.io/ollama-helm/
```
```
helm repo update
```
```
helm install ollama ollama-helm/ollama --namespace stk-helm-ollama --values ollama-values.yaml
```
- Once more, ensure you are in the kubernetes directory of this repository as instructed above. Now that each helm-initiated pod is spun up, we must apply the necessary files on kubernetes to have everything running on your local cluster:
```
kubectl apply -f aiclient-deployment.yaml -f aiclient-service.yaml -f aiclient-configmap.yaml -n stk-aimicroservice
```
```
kubectl apply -f db-deployment.yaml -f db-service.yaml -f db-configmap.yaml -n stk-dbmicroservice
```
```
kubectl apply -f frontend-deployment.yaml -f frontend-service.yaml -n stk-frontendmicroservice
```
- You must also port-forward each microservice like so:
```
kubectl port-forward -n stk-aimicroservice service/aiclient-service 8080:8080
```
```
kubectl port-forward -n stk-dbmicroservice service/stock-app-service 5000:5000
```
```
kubectl port-forward -n stk-frontendmicroservice service/frontend-service 5010:5010
```
- Once each microservice is port-forwarded, you can use the IP address listed upon port-forwarding to create Postman Routes under a given collection. Documentation on using Postman is provided in the Sources section if there are any questions on creating a Postman Collection. The routes accessed are indicated in the following links sequentially for your collection:
    1. http://127.0.0.1:5000/start_fetching - This route will initiate the stock-data fetching process.
    2. http://127.0.0.1:5000/all_stock_data - This will display the fetched stock-data in JSON format.
    3. http://127.0.0.1:8080/ai/generate/beginConversation - This route begins the conversation with Mistral.
    4. http://127.0.0.1:8080/ai/generate/introduceAssignment - This route lets Mistral know what it must do for the Blog Post.
    5. http://127.0.0.1:8080/ai/generate/updateData - You can provide the stored Stock Data from Step 2 as a parameter to this route on your Postman Collection.
    6. http://127.0.0.1:8080/ai/generate/firstPrompt - This route will generate the first-prompt and provide the AI Analysis that needs to be sent to the Blog-Post Front-End.
    7. http://127.0.0.1:5010/postdata - You can provide the AI output from the previous route to this route as a parameter for the front-end to be displayed.
    8. http://127.0.0.1:5010/ - You can use this to then view your Stock UI Static HTML page with the new Blog Post.
    9. For more blog posts to be generated: Repeat steps 1, 2, 5, and run this route for a new AI Post to be generated: http://127.0.0.1:8080/ai/generate/subsequentPrompts
    10. You can then use step 7 and 8 to view updated blog posts after doing step 9.
 # Executing Builds
 - If you make any changes to the AIClientMicroservice, you must execute the following to update the application as a whole on Kubernetes:
```
./gradlew clean
```
```
./gradlew build
```
```
docker build -t (YOUR DOCKERHUBNAME)/(IMAGETAG):(VERSIONTAG) .
```
```
docker login
```
```
docker push
```
- Change the container name in the aiclient-deployment.yaml to your Dockerhub Container name you pushed to dockerhub.
- If you make any changes to DBMicroservice or Front-End Microservice execute the following builds:
```
docker build -t (YOUR DOCKERHUBNAME)/(IMAGETAG):(VERSIONTAG) .
```
```
docker login
```
```
docker push
```
- Once more, change the container name in the frontend-deployment.yaml and or db-deployment.yaml to your container image name on Dockerhub. Be certain of the version tags matching!
# Sample Screenshot of Functioning Blog Post
<img width="1208" alt="Screen Shot 2024-05-07 at 11 39 44 AM" src="https://github.com/saqanj/Stocker/assets/134897920/5ed860af-08cf-4761-a5ff-09e3faf0f07b">

  
# Lessons Learned & Project Recap
- CI/CD Pipelines! Having automated CI/CD Pipelines for building Docker Containers, and re-applying Kubernetes files is a MUST! This project was done using manual build and re-deployments and it was a huge hassle. A future iteration of this might have Github Workflows to handle this.
- Know your cluster limits! Had we known about the GKE Hardware Limitations earlier, we would have had a completely different architecture for our project than was initially saught out. 
- Teamwork makes the dreamwork! "The true Stocker AI was the friends we made along the way" - Kwadwo. This project would not have been possible given the insane turbulence with Ollama and how we had originally envisioned using Ghost as our front-end. Having teammates to grind with you into the late hours of the night for a project to work is a crucial thing.
- Know your dependencies! In addition to the hardware limitations with Ollama, we had not anticipated that Ghost would give so much trouble with implementation on the class cluster because of ephimeral storage. This took a huge chunk of time out of our project, and would have been better spent had we anticipated this occuring. 
- Software is all about adapting! Given our original implementation was no longer working, my group had to be incredibly agile and adaptive to the situation we were in. We had two choices, either present a failing product, or work hard through to the very deadline to make sure we can have THE MOST functioning product possible to demonstrate to the class. Going as far as to creating a new microservice from scratch right before the deadline and a brand new project repository with completely new documentation. 

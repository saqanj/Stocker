package cpsc415.AIClientMicroservice;

import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.ollama.OllamaChatClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.json.JSONObject;

@SpringBootApplication
@RestController
public class ChatController {


	public static void main(String[] args) {
		SpringApplication.run(ChatController.class, args);
	}


	private final OllamaChatClient chatClient;

	@Autowired
	public ChatController(OllamaChatClient chatClient) {
		this.chatClient = chatClient;
	}

	public String data = "This is empty!";

	@GetMapping("/ai/generate/beginConversation")
	public String beginConversation(){
		return chatClient.call(new Prompt("Hello!")).getResult().getOutput().getContent();
	}

	@GetMapping("/ai/generate/introduceAssignment")
	public String introduceAssignment(){
		return chatClient.call(new Prompt("Imagine you are a stock investment blogger! I " +
				"am about to send stock data from the last hour in a subsequent prompt, " +
				"and you will have to " +
				"provide me with a response that analyzes the stock data for these " +
				"exact trends you will be reporting on:\n" +
				"1. A Short-Term Investing Perspective (Volatility and Price Movement)\n" +
				"2. Describe Trading Volume of each stock to gauge Liquidity and Investor Interest.\n" +
				"3. Sector Performance\n" +
				"4. Given the previous three trends, describe your recommendation " +
				"for the overall best stock at the moment as well as remarks on " +
				"overall market trends from " +
				"the last hour (bull/bear?).\n" +
				"\n" +
				"Respond saying \"Alright.\" once you have registered this information, " +
				"and I will send the data to which you must respond! Do not analyze anything " +
				"until the data has " +
				"been sent. Thanks!")).getResult().getOutput().getContent();
	}


	@GetMapping("/ai/generate/firstPrompt")
	public String firstPrompt() {
		return chatClient.call(new Prompt("Remember to not make any reference to this conversation, and provide a clear " +
				"response as if you were an online stock blogger. Embody the persona of a stock blogger fully. " +
				"Even if there is not enough data to make a full analysis, just do the best you " +
				"can and do not comment on how there is not enough data. Just report on what you can." +
				"Thanks! Here is the data:" + data)).getResult().getOutput().getContent();
	}

	@PostMapping("/ai/generate/updateData")
	public String firstPromptWithJson(@RequestBody String stockData) {
		data = stockData;
		return "JSON data received and stored successfully!";
	}

	@GetMapping("/ai/generate/subsequentPrompts")
	public String subsequentPrompts(){
		return chatClient.call(new Prompt("Generate the same " +
				"format of analysis as before on the following " +
				"data:" + data)).getResult().getOutput().getContent();
	}
}
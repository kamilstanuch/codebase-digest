## Generate API Client Code 

**Objective:** Generate client-side code in a specified programming language (e.g., JavaScript, Python) that can interact with an API, given the API specification or a codebase implementing the API. 

**Instructions:**

1. **Access the API definition:**  Obtain the API specification (e.g., OpenAPI/Swagger definition) or access the codebase that implements the API.
2. **Determine the target language:** Use the specified programming language for the generated client code.
3. **Generate the client code:**  
    * **API Methods:** Generate functions or methods for each API endpoint (e.g., `getUser(userId)`, `createOrder(orderData)`).
    * **Data Models:**  Create data structures or classes that represent request and response payloads for API interactions, matching the API specification. 
    * **Authentication:** If the API requires authentication, include necessary authentication mechanisms (e.g., API keys, OAuth) in the generated code. 
    * **Error Handling:** Implement robust error handling to handle different API response codes (e.g., 400 Bad Request, 500 Server Error) and provide helpful error messages. 
4. **Ensure code quality:** The generated code should be: 
    * **Readable and Well-Formatted:** Follow coding conventions and style guides for the target language.
    * **Well-Documented:**  Include comments to explain the purpose of different methods, classes, and how to use the client code.

**Expected Output:** Working API client code in the specified programming language that can:

* Authenticate with the API (if required). 
* Make requests to different API endpoints.
* Handle responses and errors gracefully.
* Be easily integrated into a larger project. 

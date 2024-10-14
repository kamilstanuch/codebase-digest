## API Conformance Check

**Objective:** Given an API specification, analyze a codebase to identify any inconsistencies or deviations from the defined API contract.

**Instructions:**

1. **Obtain the API specification:**  Access the API definition in a suitable format (e.g., YAML, JSON).
2. **Map API endpoints to code:**  Identify the code modules or functions responsible for handling each API endpoint defined in the specification.
3. **Compare the API specification with the codebase implementation:**
    * **HTTP Methods:**  Verify that the implemented methods (GET, POST, PUT, DELETE, etc.) match those defined for each endpoint.
    * **Request Parameters:**  Check that the code handles all required and optional parameters as specified.
    * **Request and Response Bodies:**  Ensure that the data structures used in the code for request and response payloads match the data models defined in the specification. 
    * **Error Handling:**  Verify that the code returns the correct HTTP status codes and error responses for different scenarios, as defined in the specification. 
4. **Document inconsistencies:**
    * Clearly describe any discrepancies found between the API specification and the code implementation.
    * Provide specific code examples and line numbers where the deviations occur.
5. **Assess the severity of inconsistencies:** Determine if the inconsistencies are: 
    * Minor (e.g., differences in parameter naming)
    * Major (e.g., missing endpoints, different data structures).

**Expected Output:** A detailed report that:

1. Lists all identified inconsistencies between the API specification and the codebase.
2. Provides a clear description of each inconsistency, its location in the code, and its potential severity. 
3. Helps prioritize fixes by highlighting major conformance issues. 

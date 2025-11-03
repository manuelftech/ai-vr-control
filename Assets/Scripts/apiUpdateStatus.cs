using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Text;

public class PostDataManager : MonoBehaviour
{
    // Define the URL of your endpoint
    // curl -iX POST http://localhost:5000/game-objects/status -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"prompt": "test"}'

    public string apiURL = "http://localhost:5000/game-objects/status";

    void Start()
    {
        // Call the coroutine when the object starts
        StartCoroutine(SendPostRequest());
    }

    IEnumerator SendPostRequest()
    {
        // 1. Create the data payload as a C# class (optional, but cleaner)
        // You would typically define a class matching your JSON structure:
        // [System.Serializable]
        // public class UserData { public string username; public int age; }
        // UserData user = new UserData { username = "jdoe", age = 30 };
        // string jsonData = JsonUtility.ToJson(user);

        // For this example, we'll use a raw JSON string:
        string jsonData = "{\"prompt\":\"increase the gravity of all the green objects that are near the chair\"}";

        // 2. Convert the JSON string to a byte array
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);

        // 3. Create the UnityWebRequest object
        using (UnityWebRequest request = new UnityWebRequest(apiURL, "POST"))
        {
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            
            // 4. Set the necessary Content-Type header to tell the server it's JSON
            request.SetRequestHeader("Content-Type", "application/json");

            // 5. Send the request and wait for a response
            yield return request.SendWebRequest();

            // 6. Check for errors
            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + request.error);
            }
            else
            {
                // 7. Success: Log the response received from the server
                Debug.Log("Received: " + request.downloadHandler.text);
            }
        }
    }
}

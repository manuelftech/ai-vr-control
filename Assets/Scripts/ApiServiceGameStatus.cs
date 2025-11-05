using UnityEngine;
using UnityEngine.Networking;
using System.Threading.Tasks;
using System.Collections.Generic;

public class ApiServiceGameStatus : MonoBehaviour
{
    public string apiURL = "http://localhost:5000/game-objects/status";
    public async void CallEndpointGameStatus()
    {
        string jsonData = "{\"prompt\":\"increase the gravity of all the green objects that are near the chair\"}";
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
        using (UnityWebRequest request = new UnityWebRequest(apiURL, "POST"))
        {
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            yield return request.SendWebRequest();
            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + request.error);
            }
            else
            {
                Debug.Log("API CallEndpointGameStatus Response: " + request.downloadHandler.text);
                return JsonUtility.FromJson<GameStatusAPIResponse>(UnityWebRequest.downloadHandler.text);
            }
        }
    }
}
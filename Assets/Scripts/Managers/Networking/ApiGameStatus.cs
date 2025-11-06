using UnityEngine;
using UnityEngine.Networking;
using System.Text;
using System.Threading.Tasks;
using System.Collections.Generic;
using AIControlMagicVR.Data.Models;
using System;

namespace AIControlMagicVR.Managers.Networking
{
    public class APIChatbotExecuteAction : MonoBehaviour
    {
        public string apiURL = "http://localhost:5000/game-objects/status";
        // curl -iX POST http://localhost:5000/game-objects/status -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"prompt": "test"}'
        public async Task<ObjectsProperties> CallEndpointGameStatus(APIChatbotRequest chatbotRequest)
        {
            // byte[] bodyRaw = Encoding.UTF8.GetBytes("{'Prompt':'increase the gravity of all the green objects that are near the chair', 'GameObjectsProperties': " + gameObjectsProperties + "}");
            // request.uploadHandler = new UploadHandlerRaw(bodyRaw);

            using UnityWebRequest request = new UnityWebRequest(apiURL, "POST");
            request.uploadHandler = new UploadHandlerRaw(chatbotRequest);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            await request.SendWebRequest();
            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + request.error);
                throw new Exception("Error: " + request.error);
            }
            else
            {
                Debug.Log("API CallEndpointGameStatus Response: " + request.downloadHandler.text);
                return JsonUtility.FromJson<ObjectsProperties>(request.downloadHandler.text);
            }
        }
    }
}
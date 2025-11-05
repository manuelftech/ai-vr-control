using UnityEngine;
using UnityEngine.Networking;
using System.Text;
using System.Threading.Tasks;
using System.Collections.Generic;
using AIControlMagicVR.Data.Models;
using System;
 
namespace AIControlMagicVR.Managers.Networking
{
    public class ApiServiceGameStatus : MonoBehaviour
    {
        public string apiURL = "http://localhost:5000/game-objects/status";
        public async Task<ElementsStatus> CallEndpointGameStatus()
        {
            string jsonData = "{\"prompt\":\"increase the gravity of all the green objects that are near the chair\"}";
            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
            using UnityWebRequest request = new UnityWebRequest(apiURL, "POST");
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
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
                return JsonUtility.FromJson<ElementsStatus>(request.downloadHandler.text);
            }
        }
    }
}
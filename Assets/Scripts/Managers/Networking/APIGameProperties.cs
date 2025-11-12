using UnityEngine;
using UnityEngine.Networking;
using System.Text;
using System.Threading.Tasks;
using System.Collections.Generic;
using AIControlMagicVR.Data.Models;
using System;
using Newtonsoft.Json;

using System.Reflection;

namespace AIControlMagicVR.Managers.Networking
{
    public class APIGameProperties
    {
        public string apiURL = "http://localhost:5000/game-objects/status";
        public async Task<ObjectsProperties> CallChatbotExecuteAction(APIChatbotRequest chatbotRequest)
        {
            // byte[] bodyRaw = Encoding.UTF8.GetBytes("{'Prompt':'increase the gravity of all the green objects that are near the chair', 'GameObjectsProperties': " + gameObjectsProperties + "}");
            // request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            var jsonRequest = JsonConvert.SerializeObject(chatbotRequest);
            Debug.Log("[APIGameProperties] API Request: " + jsonRequest);

            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonRequest);
            using UnityWebRequest request = new UnityWebRequest(apiURL, "POST");
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            await request.SendWebRequest();
            if (request.result != UnityWebRequest.Result.Success)
            {
                throw new Exception("[APIGameProperties] Error: " + request.error);
            }
            else
            {
                Debug.Log("[APIGameProperties] API Response: " + request.downloadHandler.text);
                var response = JsonUtility.FromJson<ObjectsProperties>(request.downloadHandler.text);
                Debug.Log("[APIGameProperties] Conversion completed");
                return response;
            }
        }
    }
}
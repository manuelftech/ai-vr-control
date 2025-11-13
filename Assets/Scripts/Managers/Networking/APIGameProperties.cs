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
    public class APIVRProperties
    {
        public string apiURL = "http://localhost:5000/virtual-reality-environment/state";
        public async Task<ObjectsProperties> CallChatbotExecuteAction(APIChatbotRequest chatbotRequest)
        {
            var jsonRequest = JsonConvert.SerializeObject(chatbotRequest);
            Debug.Log("[APIVRProperties] API Request: " + jsonRequest);

            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonRequest);
            using UnityWebRequest request = new UnityWebRequest(apiURL, "POST");
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            await request.SendWebRequest();
            if (request.result != UnityWebRequest.Result.Success)
            {
                throw new Exception("[APIVRProperties] Error: " + request.error);
            }
            else
            {
                Debug.Log("[APIVRProperties] API Response: " + request.downloadHandler.text);
                var response = JsonUtility.FromJson<ObjectsProperties>(request.downloadHandler.text);
                Debug.Log("[APIVRProperties] Conversion completed");
                return response;
            }
        }
    }
}
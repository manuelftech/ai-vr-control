using AIControlMagicVR.Data.Models;
using System.Collections.Generic;
using AIControlMagicVR.Managers;
using System.Threading.Tasks;
using UnityEngine.Networking;
using System.Reflection;
using Newtonsoft.Json;
using System.Text;
using UnityEngine;
using System;

namespace AIControlMagicVR.Managers.Networking
{
    public class APIVRProperties
    {
        public async Task<ObjectsProperties> CallChatbotExecuteAction(APIChatbotRequest chatbotRequest)
        {
            var jsonRequest = JsonConvert.SerializeObject(chatbotRequest);
            Debug.Log($"API Request: {jsonRequest}");

            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonRequest);
            string apiURL = GlobalManager.Instance.ApiURL;
            Debug.Log($"Endpoint URL: {apiURL}");
            using UnityWebRequest request = new UnityWebRequest(apiURL, "POST");
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            await request.SendWebRequest();
            if (request.result != UnityWebRequest.Result.Success)
            {
                throw new Exception($"Error calling API Endpoint: {request.error}");
            }
            else
            {
                Debug.Log($"API Response: {request.downloadHandler.text}");
                var response = JsonUtility.FromJson<ObjectsProperties>(request.downloadHandler.text);
                return response;
            }
        }
    }
}
using AIControlVR.Data.Models;
using System.Collections.Generic;
using AIControlVR.Managers;
using System.Threading.Tasks;
using UnityEngine.Networking;
using System.Reflection;
using Newtonsoft.Json;
using System.Text;
using UnityEngine;
using System;

namespace AIControlVR.Managers.Networking
{
    public class APIVRProperties
    {
        public async Task<TransformResponse> UpdateVRStatus(APIChatbotRequest chatbotRequest)
        {
            var jsonRequest = JsonConvert.SerializeObject(chatbotRequest);
            Debug.Log($"API Request: {jsonRequest}");

            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonRequest);
            string ApiURL = GlobalManager.Instance.ApiURL;
            Debug.Log($"State Endpoint URL: {ApiURL}");
            using UnityWebRequest request = new UnityWebRequest(ApiURL, "PUT");
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            await request.SendWebRequest();
            if (request.result != UnityWebRequest.Result.Success)
            {
                throw new Exception($"Error calling API State Endpoint: {request.error}");
            }
            else
            {
                Debug.Log($"API State Response: {request.downloadHandler.text}");
                var response = JsonUtility.FromJson<TransformResponse>(request.downloadHandler.text);
                return response;
            }
        }

        public async Task SaveInitialVrStatus(List<ObjectProperties> virtualRealityState)
        {
            var jsonRequest = JsonConvert.SerializeObject(virtualRealityState);
            Debug.Log($"API Request: {jsonRequest}");

            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonRequest);
            string ApiURL = GlobalManager.Instance.ApiURL;
            Debug.Log($"State Endpoint URL: {ApiURL}");
            using UnityWebRequest request = new UnityWebRequest(ApiURL, "POST");
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            await request.SendWebRequest();
            if (request.result != UnityWebRequest.Result.Success)
            {
                throw new Exception($"Error calling API Endpoint: {request.error}");
            }
            Debug.Log($"Data successfully saved to Redis");
        }
    }
}
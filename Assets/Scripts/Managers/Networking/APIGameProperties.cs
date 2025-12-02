using AIControlVR.Data.Models;
using System.Collections.Generic;
using AIControlVR.Managers;
using System.Threading.Tasks;
using UnityEngine.Networking;
using System.Reflection;
using Newtonsoft.Json;
using AIControlVR;
using System.Text;
using UnityEngine;
using System;

namespace AIControlVR.Managers.Networking
{
    public class APIVRProperties
    {
        public Config Config;
        public async Task<VRStateResponse> UpdateVRStates(APIChatbotRequest chatbotRequest)
        {
            // Updates the virtual reality state in Redis
            var jsonRequest = JsonConvert.SerializeObject(chatbotRequest);
            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonRequest);
            string ApiURL = Config.ApiURL;
            Debug.Log($"Updating vr states. Endpoint URL: {ApiURL}, Request: {jsonRequest}");
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
                var response = JsonUtility.FromJson<VRStateResponse>(request.downloadHandler.text);
                return response;
            }
        }

        public async void SaveInitialVrState(List<ObjectProperties> virtualRealityState)
        {
            // Saves the initial virtual reality state in Redis
            var jsonRequest = JsonConvert.SerializeObject(virtualRealityState);
            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonRequest);
            string ApiURL = Config.ApiURL;
            Debug.Log($"Sending vr states. Endpoint URL: {ApiURL}, Request: {jsonRequest}");
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

        public async void DeleteVrStateCache(List<ObjectProperties> virtualRealityState)
        {
            // Flushes the Redis database
            string ApiURL = Config.ApiURL;
            Debug.Log($"Deleting cache data. Endpoint URL: {ApiURL}");
            using UnityWebRequest request = new UnityWebRequest(ApiURL, "DELETE");
            request.SetRequestHeader("Content-Type", "application/json");
            await request.SendWebRequest();
            if (request.result != UnityWebRequest.Result.Success)
            {
                throw new Exception($"Error calling Cache deletion API: {request.error}");
            }
            Debug.Log($"Cache data successfully deleted");
        }
    }
}
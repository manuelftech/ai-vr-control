using System.Collections.Generic;
using AIControlVR.Configuration;
using AIControlVR.Data.Models;
using System.Threading.Tasks;
using UnityEngine.Networking;
using System.Reflection;
using Newtonsoft.Json;
using System.Text;
using System.Linq;
using UnityEngine;
using System;
using TMPro;

namespace AIControlVR.Managers.Networking
{
    public class APIVRProperties
    {
        public Config Config;
        private const float waitingSecondsLoading = 0.2f;
        private const int loadingMessageLength = 5;
        public async Task<VRStateResponse> UpdateVRStates(APIChatbotRequest chatbotRequest)
        {
            // Updates the virtual reality state in Redis
            var jsonRequest = JsonConvert.SerializeObject(chatbotRequest);
            Debug.Log($"Updating vr states. Endpoint URL: {Config.ApiStates}, Request: {jsonRequest}");
            using UnityWebRequest request = new UnityWebRequest(Config.ApiStates, "PUT");
            request.uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(jsonRequest));
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            request.SetRequestHeader("Authorization", $"Bearer {Config.AuthenticationToken}");
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
            Debug.Log($"Sending vr states. Endpoint URL: {Config.ApiStates}, Request: {jsonRequest}");
            using UnityWebRequest request = new UnityWebRequest(Config.ApiStates, "POST");
            request.uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(jsonRequest));
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            request.SetRequestHeader("Authorization", $"Bearer {Config.AuthenticationToken}");
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
            Debug.Log($"Deleting cache data. Endpoint URL: {Config.ApiStates}");
            using UnityWebRequest request = new UnityWebRequest(Config.ApiStates, "DELETE");
            request.SetRequestHeader("Content-Type", "application/json");
            request.SetRequestHeader("Authorization", $"Bearer {Config.AuthenticationToken}");
            await request.SendWebRequest();
            if (request.result != UnityWebRequest.Result.Success)
            {
                throw new Exception($"Error calling Cache deletion API: {request.error}");
            }
            Debug.Log("Cache data successfully deleted");
        }

        
        public IEnumerator<WaitForSeconds> UpdateTextStateStream(TextMeshPro textComponent, APIChatbotRequest request)
        {
            using (UnityWebRequest webRequest = new UnityWebRequest(Config.ApiTextStreaming, "POST"))
            {
                Debug.Log($"Calling streaming endpoint {Config.ApiTextStreaming}");
                webRequest.uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(request)));
                webRequest.downloadHandler = new DownloadHandlerBuffer();
                webRequest.SetRequestHeader("Content-Type", "application/json");
                webRequest.SetRequestHeader("Authorization", $"Bearer {Config.AuthenticationToken}");
                webRequest.SendWebRequest();

                // Displays the loading bar for the user
                while (!webRequest.isDone && webRequest.downloadHandler.text.Length < 1){
                    if (textComponent.text.Length == loadingMessageLength) textComponent.text = string.Empty;
                    textComponent.text += Config.DefaultWaitingMessageSymbol;
                    yield return new WaitForSeconds(waitingSecondsLoading);
                }
                
                // Receives the streaming text from the API
                textComponent.text = string.Empty;
                string previousResponse = string.Empty;
                while (!webRequest.isDone)
                {
                    if (webRequest.downloadHandler.text != previousResponse)
                    {
                        textComponent.text += webRequest.downloadHandler.text.Substring(previousResponse.Length);
                        previousResponse = webRequest.downloadHandler.text;
                    }
                    yield return null;
                }
                if (webRequest.result != UnityWebRequest.Result.Success) throw new Exception($"Error calling information streaming API: {webRequest.error}");
                if (webRequest.downloadHandler.text != previousResponse)
                {
                    textComponent.text += webRequest.downloadHandler.text.Substring(previousResponse.Length); 
                }
                Debug.Log($"Information streaming completed. Complete Text: {textComponent.text}");
            }
        }
        
    }
}
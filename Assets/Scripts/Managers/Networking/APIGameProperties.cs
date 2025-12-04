using AIControlVR.Data.Models;
using System.Collections.Generic;
using System.Threading.Tasks;
using UnityEngine.Networking;
using System.Reflection;
using Newtonsoft.Json;
using AIControlVR;
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
        private const int rangeLoading = 30;
        private const int maxRange = 5;
        private const string loadingSeparator = ".";
        public async Task<VRStateResponse> UpdateVRStates(APIChatbotRequest chatbotRequest)
        {
            // Updates the virtual reality state in Redis
            var jsonRequest = JsonConvert.SerializeObject(chatbotRequest);
            Debug.Log($"Updating vr states. Endpoint URL: {Config.ApiStates}, Request: {jsonRequest}");
            using UnityWebRequest request = new UnityWebRequest(Config.ApiStates, "PUT");
            request.uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(jsonRequest));
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
            Debug.Log($"Sending vr states. Endpoint URL: {Config.ApiStates}, Request: {jsonRequest}");
            using UnityWebRequest request = new UnityWebRequest(Config.ApiStates, "POST");
            request.uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(jsonRequest));
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
            Debug.Log($"Deleting cache data. Endpoint URL: {Config.ApiStates}");
            using UnityWebRequest request = new UnityWebRequest(Config.ApiStates, "DELETE");
            request.SetRequestHeader("Content-Type", "application/json");
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
                webRequest.SendWebRequest();

                // Displays the loading bar for the user
                textComponent.text = string.Empty;
                foreach (int _ in Enumerable.Range(0, rangeLoading)){
                    if(textComponent.text.Length == loadingMessageLength) textComponent.text = string.Empty;
                    textComponent.text += Config.DefaultWaitingMessageSymbol;
                    yield return new WaitForSeconds(waitingSecondsLoading);
                }

                // Displays the prompt sent by the user
                textComponent.text = string.Empty;
                var waitingMessage = String.Format(Config.AgentLoadingMessage, request.Prompt).Split(" ");
                foreach (string word in waitingMessage){
                    textComponent.text += word.Contains("\n") ? word : $"{word} ";
                    yield return new WaitForSeconds(waitingSecondsLoading);
                }

                // Displays the loading text for the user
                foreach (int range in Enumerable.Range(0, maxRange)){
                    if(range == 0) textComponent.text += " ";
                    if(range > 0) textComponent.text += loadingSeparator;
                    if (range == maxRange -1) textComponent.text += " ";
                    yield return new WaitForSeconds(waitingSecondsLoading * 2);
                }

                // Receives the streaming text from the API
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
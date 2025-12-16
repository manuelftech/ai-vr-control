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
    public class AgentAPI
    {
        public Config Config;
        private const float waitingSecondsLoading = 0.4f;
        private const int loadingMessageLength = 4;
        public async Task<VRStateResponse> UpdateVRStates(APIStateRequest apiStateRequest)
        {
            // Updates the virtual reality state in Redis
            string method = "PUT";
            var jsonRequest = JsonConvert.SerializeObject(apiStateRequest);
            Debug.Log($"Endpoint URL: {Config.ApiSessionStates}, Method: {method} Request: {jsonRequest}");
            using UnityWebRequest request = new UnityWebRequest(Config.ApiTemplate, method);
            request.uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(jsonRequest));
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            await request.SendWebRequest();
            if (request.result != UnityWebRequest.Result.Success)
            {
                throw new Exception($"Error calling API State Endpoint {Config.ApiTemplate}: Error: {request.error}");
            }
            else
            {
                Debug.Log($"Endpoint URL: {Config.ApiTemplate}, Method: {method} Response: {request.downloadHandler.text}");
                var response = JsonUtility.FromJson<VRStateResponse>(request.downloadHandler.text);
                return response;
            }
        }

        public async Task<ConversationStateResponse> SaveInitialVrState(ObjectsProperties objectsProperties)
        {
            // Saves the initial virtual reality state in Redis
            string method = "POST";
            var jsonRequest = JsonConvert.SerializeObject(objectsProperties);
            Debug.Log($"Endpoint URL: {Config.ApiSessionStates}, Method: {method} Request: {jsonRequest}");
            using UnityWebRequest request = new UnityWebRequest(Config.ApiSessionStates, method);
            request.uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(jsonRequest));
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            await request.SendWebRequest();
            if (request.result != UnityWebRequest.Result.Success)
            {
                throw new Exception($"Error calling API State Endpoint {Config.ApiSessionStates}: Error: {request.error}");
            }
            Debug.Log($"Endpoint URL: {Config.ApiSessionStates}, Method: {method}, Response: {request.downloadHandler.text}");
            var response = JsonUtility.FromJson<ConversationStateResponse>(request.downloadHandler.text);
            return response;
        }

        public async void DeleteVrStateCache(CacheDeletionRequest cacheDeletionRequest)
        {
            // Flushes the Redis database
            string method = "DELETE";
            var jsonRequest = JsonConvert.SerializeObject(cacheDeletionRequest);
            Debug.Log($"Endpoint URL: {Config.ApiSessionStates}, Method: {method} Request: {jsonRequest}");
            using UnityWebRequest request = new UnityWebRequest(Config.ApiSessionStates, method);
            request.uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(jsonRequest));
            request.SetRequestHeader("Content-Type", "application/json");
            await request.SendWebRequest();
            if (request.result != UnityWebRequest.Result.Success)
            {
                throw new Exception($"Error calling API State Endpoint {Config.ApiSessionStates}: Error: {request.error}");
            }
            Debug.Log($"Endpoint URL: {Config.ApiSessionStates}, Method: {method} Successfully deleted cache.");
        }
        
        public IEnumerator<WaitForSeconds> UpdateTextStateStream(TextMeshPro textComponent, APIStateRequest apiStateRequest)
        {
            string method = "POST";
            var jsonRequest = JsonConvert.SerializeObject(apiStateRequest);
            using (UnityWebRequest webRequest = new UnityWebRequest(Config.ApiSessionStatesStream, "POST"))
            {
                Debug.Log($"Endpoint URL: {Config.ApiSessionStatesStream}, Method: {method} Request: {jsonRequest}");
                webRequest.uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(jsonRequest));
                webRequest.downloadHandler = new DownloadHandlerBuffer();
                webRequest.SetRequestHeader("Content-Type", "application/json");
                webRequest.SendWebRequest();

                // Displays the loading bar for the user
                textComponent.text = string.Empty;
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
                        Debug.Log($"Receiving streaming info: {webRequest.downloadHandler.text}");
                    }
                    yield return null;
                }
                if (webRequest.result != UnityWebRequest.Result.Success) throw new Exception($"Error calling API State Endpoint {Config.ApiSessionStatesStream}: Error: {webRequest.error}");
                if (webRequest.downloadHandler.text != previousResponse)
                {
                    textComponent.text += webRequest.downloadHandler.text.Substring(previousResponse.Length); 
                }
                Debug.Log($"Endpoint URL: {Config.ApiSessionStatesStream}, Method: {method}, Response: {textComponent.text}");
            }
        }


        public IEnumerator<object> DisplayGeneratedImage(SpriteRenderer spriteRenderer, APIStateRequest apiStateRequest)
        {
            string method = "POST";
            Debug.Log($"Endpoint URL: {Config.ApiScreenshot}, Method: {method}");
            Texture2D texture = new Texture2D(1, 1);
            using (UnityWebRequest webRequest = new UnityWebRequest(Config.ApiScreenshot, method))
            {
                webRequest.downloadHandler = new DownloadHandlerBuffer();
                yield return webRequest.SendWebRequest();
                if (webRequest.result != UnityWebRequest.Result.Success) throw new Exception($"Error calling API State Endpoint {Config.ApiSessionStatesStream}: Error: {webRequest.error}");
                texture.LoadImage(webRequest.downloadHandler.data);
                spriteRenderer.sprite = Sprite.Create(texture, new Rect(0, 0, texture.width, texture.height), new Vector2(0.5f, 0.5f), 10.0f);                    
                Debug.Log($"Displaying screenshot");
            }
        }
    }
}
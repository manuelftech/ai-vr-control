using AIControlVR.Managers.Networking;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using AIControlVR.Data.Models;
using System.Threading.Tasks;
using AIControlVR.Managers;
using AIControlVR.Configuration;
using System.Reflection;
using System.Threading;
using UnityEngine;
using System;
using TMPro;

namespace AIControlVR.Data.ScriptableObjects
{
    public class VirtualKeyboardActions : MonoBehaviour
    {
        public Config Config;
        private AgentAPI agentAPI = new AgentAPI();
        public string CaptureKeyboardInputText()
        {
            GameObject keyboardText = GameObject.FindWithTag(Config.DefaultInputTag);
            if (keyboardText == null) throw new Exception($"Element with Tag: {Config.DefaultInputTag} not found in the scene.");
            var tmpInputField = keyboardText.GetComponent<TMP_InputField>();
            if (tmpInputField == null) Debug.LogWarning($"TMPInputField component not found in Tag: : {Config.DefaultInputTag}");
            return tmpInputField.text;
        }

        public async void RequestActionToAgent()
        {
            

            bool isStreaming = GlobalManager.Instance.StreamingMode;
            if (isStreaming){
                APIStateRequest reqStreaming = new APIStateRequest.Builder()
                    .Prompt(CaptureKeyboardInputText())
                    .ConversationId(GlobalManager.Instance.ConversationIdInfo)
                    .Build();
                Debug.Log("Streaming Mode");
                StreamAgentMessage(reqStreaming);
                return;
            }
            Debug.Log("Not streaming Mode");
            // Send the prompt to te Agent
            APIStateRequest reqSynchronous = new APIStateRequest.Builder()
                    .Prompt(CaptureKeyboardInputText())
                    .ConversationId(GlobalManager.Instance.ConversationIdTemplate)
                    .Build();
            VRStateResponse response = await agentAPI.UpdateVRStates(reqSynchronous);

            // Change the state of the elements in the 3D environment
            GlobalManager.Instance.UpdateVRStateProperties(response);
        }

        public void StreamAgentMessage(APIStateRequest request)
        {
            GameObject televisionText = GameObject.FindWithTag(Config.DefaultTextDisplayTag);
            if (televisionText == null) throw new Exception($"Element with Tag: {Config.DefaultTextDisplayTag} not found in the scene.");
            TextMeshPro textComponent = televisionText.GetComponent<TextMeshPro>();
            if (textComponent == null) throw new Exception($"tmpInputField component not found in Tag: : {Config.DefaultInputTag}");
            StartCoroutine(agentAPI.UpdateTextStateStream(textComponent, request));
        }
    }
}
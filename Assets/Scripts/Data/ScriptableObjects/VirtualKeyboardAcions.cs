using AIControlVR.Managers.Networking;
using AIControlVR.Data.Models;
using AIControlVR.Managers;
using System.Reflection;
using System.Threading;
using UnityEngine;
using System;
using TMPro;

namespace AIControlVR.Data.ScriptableObjects
{
    public class VirtualKeyboardActions : MonoBehaviour
    {
        private string Tag = "keyboardText";
        private APIVRProperties apiVRProperties = new APIVRProperties();
        public string CaptureKeyboardInputText()
        {
            GameObject keyboardText = GameObject.FindWithTag(Tag);
            if (keyboardText != null)
            {
                var tmpInputField = keyboardText.GetComponent<TMP_InputField>();
                if (tmpInputField != null)
                {
                    var text = tmpInputField.text;
                    Debug.Log($"Keyboard input: {text}");
                    tmpInputField.text = "";
                    return text;
                }
                else
                {
                    Debug.LogWarning($"TMPInputField component not found in Tag: : {Tag}");
                }
            }
            throw new Exception($"Element with Tag: {this.Tag} not found in the scene."); 
        }


        public async void RequestActionToChatbot()
        {
            // Send both the prompt, and the VR states' current properties to the chatbot, to command it to calculate the new rquested properties to be assigned to these VR States
            APIChatbotRequest request = new APIChatbotRequest.Builder()
                .Prompt(this.CaptureKeyboardInputText())
                .VirtualRealityState(GlobalManager.Instance.GetFormattedVirtualRealityState())
                .Build();

            ObjectsProperties response = await apiVRProperties.CallChatbotExecuteAction(request);
            GlobalManager.Instance.UpdateVRStateProperties(response.VirtualRealityState);
        }
    }
}
using AIControlMagicVR.Managers.Networking;
using AIControlMagicVR.Data.Models;
using AIControlMagicVR.Managers;
using System.Reflection;
using System.Threading;
using UnityEngine;
using System;
using TMPro;

namespace AIControlMagicVR.Data.ScriptableObjects
{
    public class VirtualKeyboardActions : MonoBehaviour
    {
        private static readonly string Tag = "keyboardText";
        private APIVRProperties apiVRProperties = new APIVRProperties();
        public string CaptureKeyboardInputText()
        {
            GameObject keyboardText = GameObject.FindWithTag(Tag);
            if (keyboardText != null)
            {
                Debug.Log("Found the Keyboard Input GameObject");
                var tmpInputField = keyboardText.GetComponent<TMP_InputField>();
                if (tmpInputField != null)
                {
                    var text = tmpInputField.text;
                    Debug.Log("Text entered: " + text);
                    tmpInputField.text = "";
                    return text;
                }
                else
                {
                    Debug.LogError("GameObject tagged '" + Tag + "' does not have a TMP_InputField component attached!");
                    throw new Exception("GameObject tagged '" + Tag + "' does not have a TMP_InputField component attached!");
                }
            }
            else
            {
                Debug.LogWarning("No GameObject with the tag '" + Tag + "' found in the scene.");
                throw new Exception("No GameObject with the tag '" + Tag + "' found in the scene.");
            }
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
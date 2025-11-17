using UnityEngine;
using TMPro;
using System;
using System.Reflection;
using AIControlMagicVR.Managers;
using AIControlMagicVR.Data.Models;
using AIControlMagicVR.Managers.Networking;
using System.Threading;

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
            // Validate the television_text_display element:
            GameObject televisionDisplayText = GameObject.FindWithTag("television_display_text");
            if (televisionDisplayText != null)
            {
                Debug.Log("Found the Keyboard Input GameObject");
                var tmpInputField = televisionDisplayText.GetComponent<TMP_InputField>();
                if (tmpInputField != null)
                {
                    var text = tmpInputField.text;
                    Debug.Log("Text entered: " + text);
                    // 49 characters per line, 11 lines
                    var completeText = "0123456789abcdefghij0123456789abcdefghij012345678\n0123456789abcdefghij0123456789abcdefghij012345678\n0123456789abcdefghij0123456789abcdefghij012345678\n0123456789abcdefghij0123456789abcdefghij012345678\n0123456789abcdefghij0123456789abcdefghij012345678\n0123456789abcdefghij0123456789abcdefghij012345678\n0123456789abcdefghij0123456789abcdefghij012345678\n0123456789abcdefghij0123456789abcdefghij012345678\n0123456789abcdefghij0123456789abcdefghij012345678\n0123456789abcdefghij0123456789abcdefghij012345678\n0123456789abcdefghij0123456789abcdefghij012345678\n";
                    foreach (char streamingChar in completeText)
                    {
                        Thread.Sleep(100);
                        tmpInputField.text += streamingChar;
                    }
                    
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


            // Send both the prompt, and the VR states' current properties to the chatbot, to command it to calculate the new rquested properties to be assigned to these VR States
            //APIChatbotRequest request = new APIChatbotRequest();
            //request.Prompt = this.CaptureKeyboardInputText();
            //request.VirtualRealityState = GlobalManager.Instance.GetFormattedVirtualRealityState();
            //ObjectsProperties response = await apiVRProperties.CallChatbotExecuteAction(request);
            //GlobalManager.Instance.UpdateVRStateProperties(response.VirtualRealityState);
        }
    }
}
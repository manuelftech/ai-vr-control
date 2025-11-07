using UnityEngine;
using TMPro;
using System;
using AIControlMagicVR.Managers;
using AIControlMagicVR.Data.Models;
using AIControlMagicVR.Managers.Networking;

namespace AIControlMagicVR.Data.ScriptableObjects
{
    public class VirtualKeyboardActions : MonoBehaviour
    {
        private static readonly string Tag = "keyboardText";
        private APIGameProperties apiGameProperties = new APIGameProperties();
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
            // Send both the prompt, and the GameObjects' current properties to the chatbot, to command it to calculate the new rquested properties to be assigned to these GameObjects
            APIChatbotRequest request = APIChatbotRequest.Builder()
                    .Prompt(this.CaptureKeyboardInputText())
                    .GameObjects(GlobalManager.Instance.GetFormattedGameObjects()).Build();
            ObjectsProperties response = await apiGameProperties.CallChatbotExecuteAction(request);


            Debug.Log("Validation 1 [start]");
            Debug.Log(response.GameObjects);
            Debug.Log("Validation 1 [end]");
            GlobalManager.Instance.UpdateObjectsProperties(response.GameObjects);
        }
    }
}
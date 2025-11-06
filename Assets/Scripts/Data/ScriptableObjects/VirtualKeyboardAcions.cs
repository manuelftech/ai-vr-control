using UnityEngine;
using TMPro;
using System;

namespace AIControlMagicVR.Data.ScriptableObjects
{
    public class VirtualKeyboardActions : MonoBehaviour
    {
        private static readonly string Tag = "keyboardText";
        public string CaptureKeyboardInputText()
        {
            GameObject keyboardText = GameObject.FindWithTag(Tag);
            if (keyboardText != null)
            {
                Debug.Log("Found the gameObject: " + keyboardText.name);
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


        public void RequestActionToChatbot()
        {
            // // Send both the prompt, and the GameObjects' current properties to the chatbot, to command it to calculate the new rquested properties to be assigned to these GameObjects
            // var updatedObjectsProperties = APIActionRequest(ApiActionRequest.Builder()
            //         .PromptToChatbot(this.CaptureKeyboardInputText())
            //         .CurrentObjectsProperties(GlobalManager.Instance.sceneGameObjects).Build()
            //     );

            // Debug.Log("Data sent to the Endpoint");

            // GlobalManager.Instance.UpdateObjectsProperties(updatedObjectsProperties);
        }
    }
}
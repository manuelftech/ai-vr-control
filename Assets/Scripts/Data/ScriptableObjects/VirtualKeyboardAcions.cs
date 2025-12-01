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
                    return tmpInputField.text;
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
            // Send the prompt to te Agent
            VRStateResponse response = await apiVRProperties.UpdateVRStates(new APIChatbotRequest.Builder()
                    .Prompt(this.CaptureKeyboardInputText())
                    .Build());

            // Change the state of the elements in the 3D environment
            GlobalManager.Instance.UpdateVRStateProperties(response);
        }
    }
}
using UnityEngine;
using TMPro;
using System;
using AIControlMagicVR.Managers;

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


        public void RequestActionToChatbot()
        {
            // // Send both the prompt, and the GameObjects' current properties to the chatbot, to command it to calculate the new rquested properties to be assigned to these GameObjects
            // var updatedObjectsProperties = APIRequestActionToChatbot(ApiActionRequest.Builder()
            //         .PromptToChatbot(this.CaptureKeyboardInputText())
            //         .CurrentObjectsProperties(GlobalManager.Instance.sceneGameObjects).Build()
            //     );

            // Debug.Log("Data sent to the Endpoint");

            // GlobalManager.Instance.UpdateObjectsProperties(updatedObjectsProperties);




            // ############################################################################
            // TESTING: the following code is just for testing, and should be replaced for the code commented above:
            string instanceId = this.CaptureKeyboardInputText();
            Debug.Log("[VirtualKeyboardActions] InstanceId: " + instanceId);
            if (GlobalManager.Instance.sceneGameObjects.TryGetValue(instanceId, out GameObject localGameObject))
            {
                // Cange color
                Renderer renderer = localGameObject.GetComponent<Renderer>();
                if (renderer != null)
                {
                    //renderer.material.color = newGameObject.components.color;
                    renderer.material.color = Color.red;
                    Debug.Log("Changed color of object with ID " + instanceId);
                }
                else
                {
                    Debug.LogError("Object with ID " + instanceId + " has no Renderer component.");
                }

                // Change force
                ConstantForce constantForce = localGameObject.GetComponent<ConstantForce>();
                if (constantForce != null)
                {
                    //constantForce.force = newGameObject.components.constantForce;
                    constantForce.force = new Vector3(0, 9.82f, 0);
                    Debug.Log("Changed ConstantForce of object with ID " + instanceId);
                }
                else
                {
                    Debug.LogError("Object with ID " + instanceId + " has no Renderer component.");
                }
            }
            else
            {
                Debug.LogWarning("Could not find an object with ID: " + instanceId);
            }
        }
    }
}
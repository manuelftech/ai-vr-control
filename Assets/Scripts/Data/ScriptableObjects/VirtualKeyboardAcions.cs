using UnityEngine;
using TMPro;

namespace AIControlMagicVR.Data.ScriptableObjects
{
    public class VirtualKeyboardActions : MonoBehaviour
    {
        private static readonly string Tag = "keyboardText";
        public void SendTextToChatbot()
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
                }
                else
                {
                    Debug.LogError("GameObject tagged '" + Tag + "' does not have a TMP_InputField component attached!");
                }
            }
            else
            {
                Debug.LogWarning("No GameObject with the tag '" + Tag + "' found in the scene.");
            }
            Debug.Log("Text sent to chatbot");
        }
    }
}
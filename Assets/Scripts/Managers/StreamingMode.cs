using AIControlVR.Configuration;
using AIControlVR.Managers;
using UnityEngine.UI;
using UnityEngine;
using System;

namespace AIControlVR.Managers
{
    public class StreamingMode : MonoBehaviour
    {
        public Config Config;
        public void ToggleStreamingMode()
        {
            GameObject streamingKey = GameObject.FindWithTag(Config.StreamingTag);
            if (streamingKey == null) throw new Exception($"Element with Tag: {Config.DefaultInputTag} not found in the scene.");
            var img = streamingKey.GetComponent<Image>();
            if (img == null) Debug.LogWarning($"Image component not found in Tag: : {Config.DefaultInputTag}");
            img.enabled = !img.enabled;
            GlobalManager.Instance.StreamingMode = !GlobalManager.Instance.StreamingMode;
            Debug.Log($"Streaming mode: {GlobalManager.Instance.StreamingMode}");
        }
    }
}
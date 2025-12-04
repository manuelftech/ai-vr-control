using UnityEngine;
using AIControlVR.Managers;

namespace AIControlVR.Managers
{
    public class StreamingMode : MonoBehaviour
    {
        public void ToggleStreamingMode()
        {
            GlobalManager.Instance.StreamingMode = !GlobalManager.Instance.StreamingMode;
            Debug.Log($"Streaming mode: {GlobalManager.Instance.StreamingMode}");
        }
    }
}
using UnityEngine;

namespace AIControlVR.Managers
{
    public class AddToManager : MonoBehaviour
    {
        void Start()
        {
            if (GlobalManager.Instance != null)
            {
                GlobalManager.Instance.RegisterObject(this.gameObject);
                Debug.Log($"GlobalManager registered new component. Name: {this.name}");
            }
            else
            {
                Debug.LogError($"GlobalManager has not been initialized.");
            }
        }
    }
}
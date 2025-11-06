using UnityEngine;

namespace AIControlMagicVR.Managers
{
    public class AddToManager : MonoBehaviour
    {
        void Start()
        {
            // Register this object in the GlobalManager, to modify gameObject properties
            if (GlobalManager.Instance != null)
            {
                GlobalManager.Instance.RegisterObject(this.gameObject);
                Debug.Log("[AddToManager] GameObject registered. Name: " + this.name);
            }
            else
            {
                Debug.LogError("[AddToManager] GlobalManager instance not found! Cannot register Name: " + this.name);
            }
        }
    }
}
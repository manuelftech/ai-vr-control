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
                Debug.Log("GameObject registered: " + this.name);
            }
            else
            {
                Debug.LogError("GlobalManager instance not found! Cannot register " + this.name);
            }
        }
    }
}
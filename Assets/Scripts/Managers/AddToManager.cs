using UnityEngine;

namespace AIControlMagicVR.Managers
{
    public class AddToManager : MonoBehaviour
    {
        void Start()
        {
            if (GlobalManager.Instance != null)
            {
                GlobalManager.Instance.RegisterObject(this.gameObject);
                Debug.Log("[AddToManager] VR state registered. Name: " + this.name);
            }
            else
            {
                Debug.LogError("[AddToManager] GlobalManager instance not found! Cannot register Name: " + this.name);
            }
        }
    }
}
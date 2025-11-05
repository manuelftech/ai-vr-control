using UnityEngine;
using System.Collections.Generic;

public class GlobalManager : MonoBehaviour
{
    public static GlobalManager Instance { get; private set; }
    public Dictionary<int, GameObject> sceneGameObjects = new Dictionary<int, GameObject>();
    void Awake()
    {
        // Set up the singleton instance when the scene loads
        if (Instance != null && Instance != this)
        {
            Destroy(this.gameObject);
        }
        else
        {
            Instance = this;
        }
        Debug.Log("GlobalManager instance created.");
    }

    public void RegisterObject(GameObject obj)
    {
        int id = obj.GetInstanceID();
        if (!sceneGameObjects.ContainsKey(id))
        {
            sceneGameObjects.Add(id, obj);
        }
    }
}

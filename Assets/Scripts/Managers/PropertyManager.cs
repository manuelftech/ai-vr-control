using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Text;
using System;
using System.Collections.Generic;
using System.Linq;

namespace AIControlMagicVR.Managers
{
    public class PropertyManager : MonoBehaviour
    {
        // curl -iX POST http://localhost:5000/game-objects/status -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"prompt": "test"}'
        public string apiURL = "http://localhost:5000/game-objects/status";
        private ConstantForce constantForceComponent;
        private List<int> instanceIdsList = new List<int>();
        public string targetTag = "cube";

        void Start()
        {
            Dictionary<int, GameObject> newGameObjects = new Dictionary<int, GameObject>();
            foreach (var newGameObject in newGameObjects)
            {
                Debug.Log("InstanceId: " + newGameObject.Key);
                Debug.Log("GameObject: " + newGameObject.Value);
                if (GlobalManager.Instance.sceneGameObjects.TryGetValue(newGameObject.Key, out GameObject localGameObject))
                {
                    Renderer renderer = localGameObject.GetComponent<Renderer>();
                    if (renderer != null)
                    {
                        //renderer.material.color = newGameObject.color;
                        renderer.material.color = Color.red;
                        Debug.Log("Changed color of object with ID " + newGameObject.Key);
                    }
                    else
                    {
                        Debug.LogError("Object with ID " + newGameObject.Key + " has no Renderer component.");
                    }
                }
                else
                {
                    Debug.LogWarning("Could not find an object with ID: " + newGameObject.Key);
                }
            }
        }

        // - 1) Register this Object when it starts
        // if (GlobalManager.Instance != null) {
        //     GlobalManager.Instance.RegisterObject(this.gameObject);
        // } else {
        //     Debug.LogError("GlobalManager instance not found! Cannot register " + this.name);
        // }

        // - 2) Find gameObjects based on their ID:
        // GameObject[] taggedObjects = GameObject.FindGameObjectsWithTag(targetTag);
        // if (taggedObjects.Length == 0)
        // {
        //     Debug.LogWarning("No GameObjects found with the tag: " + targetTag);
        //     return;
        // }
        // foreach (GameObject obj in taggedObjects)
        // {
        //     int id = obj.GetInstanceID();
        //     instanceIdsList.Add(id);
        //     Debug.Log("Found object: " + obj.name + " with Instance ID: " + id);
        // }
        // Debug.Log("Total objects found with tag '" + targetTag + "': " + instanceIdsList.Count);

        // - 3) Change value to make objects float:
        // constantForceComponent = GetComponent<ConstantForce>();
        // if (constantForceComponent != null)
        // {
        //     constantForceComponent.force = new Vector3(0, 9.82f, 0);
        // }
        // else
        // {
        //     Debug.LogError("ConstantForce component not found on this GameObject!");
        // }

        // - 4) Change the gameObject's color:
        // Renderer renderer = GetComponent<Renderer>();
        // if (renderer != null)
        // {
        //     renderer.material.color = Color.yellow; // Changes to a specific color
        // }

        // - 5) Call endpoint:
        // StartCoroutine(SendPostRequest());

    }

}
using UnityEngine;
using System.Collections.Generic;
using System;
using AIControlMagicVR.Data.Models;
using Newtonsoft.Json;
using System.Threading.Tasks;

namespace AIControlMagicVR.Managers
{
    public class GlobalManager : MonoBehaviour
    {
        public static GlobalManager Instance { get; private set; }
        public Dictionary<string, GameObject> sceneGameObjects = new Dictionary<string, GameObject>();

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
            string universalId = Guid.NewGuid().ToString();
            if (sceneGameObjects.TryAdd(universalId, obj))
            {
                Debug.Log("[GlobalManager] GameObject registered. Universal Id: " + universalId);
            }
            else
            {
                Debug.Log("[GlobalManager] GameObject with Universal Id: " + universalId + " already registered");
            }
        }

        public void UpdateObjectsProperties(List<ObjectsProperties> updatedGameObjects)
        {
            foreach (ObjectProperties updatedGameObject in updatedGameObjects.GetGameObjects())
            {
                if (sceneGameObjects.TryGetValue(updatedGameObject.Id, out GameObject localGameObject))
                {
                    // Change color
                    Renderer renderer = localGameObject.GetComponent<Renderer>();
                    if (renderer != null)
                    {
                        // renderer.material.color = newGameObject.components.color;
                        renderer.material.color = Color.red;
                        Debug.Log("Changed color of object with ID " + updatedGameObject.Id);
                    }
                    else
                    {
                        Debug.LogError("Object with ID " + updatedGameObject.Id + " has no Renderer component.");
                    }

                    // Change force
                    ConstantForce constantForce = localGameObject.GetComponent<ConstantForce>();
                    if (constantForce != null)
                    {
                        // constantForce.force = newGameObject.components.constantForce;
                        constantForce.force = new Vector3(0, 9.82f, 0);
                        Debug.Log("Changed ConstantForce of object with ID " + updatedGameObject.Id);
                    }
                    else
                    {
                        Debug.LogError("Object with ID " + updatedGameObject.Id + " has no Renderer component.");
                    }
                }
                else
                {
                    Debug.LogWarning("Could not find an object with ID: " + updatedGameObject.Id);
                }
            }
        }

        public ObjectsProperties GetGameObjectsProperties()
        {
            ObjectsProperties objectsProperties = new ObjectsProperties();
            foreach (var sceneGameObject in sceneGameObjects)
            {
                ConstantForce constantForce = localGameObject.GetComponent<ConstantForce>();
                Renderer renderer = localGameObject.GetComponent<Renderer>();

                objectsProperties.getGameObjects().add(ObjectProperties.Builder()
                    .Id(sceneGameObject.Key)
                    .Tag(sceneGameObject.Value.tag)
                    .Component(ObjectsProperties.ComponentsProperties.Builder()
                        .ConstantForce(ObjectsProperties.CoordinatesProperties.Builder()
                            .X(constantForce.force.x)
                            .Y(constantForce.force.y)
                            .Z(constantForce.force.z).Build())
                        .Color(renderer.material.color).Build())
                    .Transform(ObjectsProperties.CoordinatesProperties.Builder()
                        .X(sceneGameObject.Value.transform.position.x)
                        .Y(sceneGameObject.Value.transform.position.y)
                        .Z(sceneGameObject.Value.transform.position.z).Build()).Build());
            }
            return objectsProperties;
        }
    }
}

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

        public List<ObjectProperties> GetFormattedGameObjects()
        {
            List<ObjectProperties> objectsProperties = new List<ObjectProperties>();
            foreach (var sceneGameObject in sceneGameObjects)
            {
                ConstantForce constantForce = sceneGameObject.Value.GetComponent<ConstantForce>();
                Renderer renderer = sceneGameObject.Value.GetComponent<Renderer>();

                ObjectProperties props = new ObjectProperties();
                props.Id = sceneGameObject.Key;
                props.Tag = sceneGameObject.Value.tag;
                props.Name = sceneGameObject.Value.name;

                CoordinatesProperties constantForceProps = new CoordinatesProperties();
                constantForceProps.X = constantForce.force.x;
                constantForceProps.Y = constantForce.force.y;
                constantForceProps.Z = constantForce.force.z;

                ComponentsProperties components = new ComponentsProperties();
                components.ConstantForce = constantForceProps;
                components.Color = renderer.material.color.ToString();

                props.Components = components;

                CoordinatesProperties position = new CoordinatesProperties();
                position.X = sceneGameObject.Value.transform.position.x;
                position.Y = sceneGameObject.Value.transform.position.y;
                position.Z = sceneGameObject.Value.transform.position.z;

                CoordinatesProperties rotation = new CoordinatesProperties();
                rotation.X = sceneGameObject.Value.transform.rotation.x;
                rotation.Y = sceneGameObject.Value.transform.rotation.y;
                rotation.Z = sceneGameObject.Value.transform.rotation.z;

                CoordinatesProperties scale = new CoordinatesProperties();
                scale.X = sceneGameObject.Value.transform.localScale.x;
                scale.Y = sceneGameObject.Value.transform.localScale.y;
                scale.Z = sceneGameObject.Value.transform.localScale.z;

                TransformProperties transform = new TransformProperties();
                transform.Position = position;
                transform.Rotation = rotation;
                transform.Scale = scale;

                props.Transform = transform;

                objectsProperties.Add(props);
            }
            Debug.Log("[GlobalManager] Completed GetFormattedGameObjects()");
            return objectsProperties;
        }

        public void UpdateObjectsProperties(List<ObjectProperties> updatedGameObjects)
        {
            Debug.Log("[UpdateObjectsProperties] Loop");
            foreach (ObjectProperties updatedGameObject in updatedGameObjects)
            {
                if (sceneGameObjects.TryGetValue(updatedGameObject.Id, out GameObject localGameObject))
                {
                    // Change color
                    Renderer renderer = localGameObject.GetComponent<Renderer>();
                    if (renderer != null)
                    {
                        Color updatedColor;
                        ColorUtility.TryParseHtmlString(updatedGameObject.Components.Color, out updatedColor);
                        renderer.material.color = updatedColor;
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
                        constantForce.force = new Vector3(updatedGameObject.Components.ConstantForce.X, updatedGameObject.Components.ConstantForce.Y, updatedGameObject.Components.ConstantForce.Z);
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
    }
}
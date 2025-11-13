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
        public Dictionary<string, GameObject> vrStateObjects = new Dictionary<string, GameObject>();

        void Awake()
        {
            // This general VR State manager is created only once
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
            // Every time a Vr State is instantiated, it is registered in the global state manager
            string universalId = Guid.NewGuid().ToString();
            if (vrStateObjects.TryAdd(universalId, obj))
            {
                Debug.Log("[GlobalManager] VR state registered. Universal Id: " + universalId);
            }
            else
            {
                Debug.Log("[GlobalManager] VR state with Universal Id: " + universalId + " already registered");
            }
        }

        public List<ObjectProperties> GetFormattedVirtualRealityState()
        {
            List<ObjectProperties> objectsProperties = new List<ObjectProperties>();
            foreach (var sceneVRState in vrStateObjects)
            {
                ConstantForce constantForce = sceneVRState.Value.GetComponent<ConstantForce>();
                Renderer renderer = sceneVRState.Value.GetComponent<Renderer>();

                ObjectProperties props = new ObjectProperties();
                props.Id = sceneVRState.Key;
                props.Tag = sceneVRState.Value.tag;
                props.Name = sceneVRState.Value.name;

                CoordinatesProperties constantForceProps = new CoordinatesProperties();
                constantForceProps.X = constantForce.force.x;
                constantForceProps.Y = constantForce.force.y;
                constantForceProps.Z = constantForce.force.z;

                ComponentsProperties components = new ComponentsProperties();
                components.ConstantForce = constantForceProps;
                components.Color = "#" + ColorUtility.ToHtmlStringRGB(renderer.material.color);

                props.Components = components;

                CoordinatesProperties position = new CoordinatesProperties();
                position.X = sceneVRState.Value.transform.position.x;
                position.Y = sceneVRState.Value.transform.position.y;
                position.Z = sceneVRState.Value.transform.position.z;

                CoordinatesProperties rotation = new CoordinatesProperties();
                rotation.X = sceneVRState.Value.transform.rotation.x;
                rotation.Y = sceneVRState.Value.transform.rotation.y;
                rotation.Z = sceneVRState.Value.transform.rotation.z;

                CoordinatesProperties scale = new CoordinatesProperties();
                scale.X = sceneVRState.Value.transform.localScale.x;
                scale.Y = sceneVRState.Value.transform.localScale.y;
                scale.Z = sceneVRState.Value.transform.localScale.z;

                TransformProperties transform = new TransformProperties();
                transform.Position = position;
                transform.Rotation = rotation;
                transform.Scale = scale;

                props.Transform = transform;

                objectsProperties.Add(props);
            }
            Debug.Log("[GlobalManager] Completed GetFormattedVirtualRealityState()");
            return objectsProperties;
        }

        public void UpdateVRStateProperties(List<ObjectProperties> updatedVRStates)
        {
            Debug.Log("[UpdateVRStateProperties] Loop");
            foreach (ObjectProperties updatedVRState in updatedVRStates)
            {
                if (vrStateObjects.TryGetValue(updatedVRState.Id, out GameObject localGameObject))
                {
                    // Change color
                    Renderer renderer = localGameObject.GetComponent<Renderer>();
                    if (renderer != null)
                    {
                        Color updatedColor;
                        ColorUtility.TryParseHtmlString(updatedVRState.Components.Color, out updatedColor);
                        
                        renderer.material.color = updatedColor;
                        Debug.Log("Changed color of VR State with ID " + updatedVRState.Id);
                        Debug.Log(updatedColor);
                        Debug.Log("Color displayed");
                    }
                    else
                    {
                        Debug.LogError("VR State with ID " + updatedVRState.Id + " has no Renderer component.");
                    }

                    // Change constant force
                    ConstantForce constantForce = localGameObject.GetComponent<ConstantForce>();
                    if (constantForce != null)
                    {
                        constantForce.force = new Vector3(updatedVRState.Components.ConstantForce.X, updatedVRState.Components.ConstantForce.Y, updatedVRState.Components.ConstantForce.Z);
                        Debug.Log("Changed ConstantForce of VR State with ID " + updatedVRState.Id);
                    }
                    else
                    {
                        Debug.LogError("VR State with ID " + updatedVRState.Id + " has no Renderer component.");
                    }
                }
                else
                {
                    Debug.LogWarning("Could not find an VR State with ID: " + updatedVRState.Id);
                }
            }
        }
    }
}
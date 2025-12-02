using AIControlVR.Managers.Networking;
using System.Collections.Generic;
using AIControlVR;
using AIControlVR.Data.Models;
using System.Threading.Tasks;
using Newtonsoft.Json;
using UnityEngine;
using System;
using TMPro;

namespace AIControlVR.Managers
{
    public class GlobalManager : MonoBehaviour
    {
        public Config Config;
        public static GlobalManager Instance { get; private set; }
        private APIVRProperties apiVRProperties = new APIVRProperties();
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

        void Start(){
            // Start the next methods after every Start method has executed
            StartCoroutine(ConfigureScene());
        }

        void OnApplicationQuit(){
            DeleteRedisCache();
        }

        IEnumerator<WaitForEndOfFrame> ConfigureScene(){
            yield return new WaitForEndOfFrame();
            this.SaveInitialStateToRedis();
        }

        private void SaveInitialStateToRedis(){
            // Send the initial 3D VR states to Redis
            apiVRProperties.SaveInitialVrState(this.GetFormattedVirtualRealityState());
        }

        private void DeleteRedisCache(){
            // Cleans cache in Redis
            apiVRProperties.DeleteVrStateCache(this.GetFormattedVirtualRealityState());
        }

        public void RegisterObject(GameObject obj)
        {
            // Every time a Vr State is instantiated, it is registered in the global state manager
            string universalId = Guid.NewGuid().ToString();
            if (vrStateObjects.TryAdd(universalId, obj))
            {
                Debug.Log($"GlobalManager VR state registered. Universal Id: {universalId}");
            }
            else
            {
                Debug.Log($"GlobalManager VR state with Universal Id: {universalId} already registered.");
            }
        }

        public List<ObjectProperties> GetFormattedVirtualRealityState()
        {
            List<ObjectProperties> objectsProperties = new List<ObjectProperties>();
            foreach (var sceneVRState in vrStateObjects)
            {
                CoordinatesProperties position = new CoordinatesProperties.Builder()
                    .X(sceneVRState.Value.transform.position.x)
                    .Y(sceneVRState.Value.transform.position.y)
                    .Z(sceneVRState.Value.transform.position.z)
                    .Build();

                CoordinatesProperties rotation = new CoordinatesProperties.Builder()
                    .X(sceneVRState.Value.transform.rotation.x)
                    .Y(sceneVRState.Value.transform.rotation.y)
                    .Z(sceneVRState.Value.transform.rotation.z)
                    .Build();

                CoordinatesProperties scale = new CoordinatesProperties.Builder()
                    .X(sceneVRState.Value.transform.localScale.x)
                    .Y(sceneVRState.Value.transform.localScale.y)
                    .Z(sceneVRState.Value.transform.localScale.z)
                    .Build();

                const float NormalSize = 1.0f;
                TransformProperties transform = new TransformProperties.Builder()
                    .Position(position)
                    .Rotation(rotation)
                    .Scale(scale)
                    .Reshape(NormalSize)
                    .Build();

                // Obtain the hexadecimal formatted color of the Renderer Component (e.g, #FFFFFF)
                Renderer renderer = sceneVRState.Value.GetComponent<Renderer>();
                string formattedColor = "";
                if(renderer?.material.HasProperty("_Color") == true){
                    formattedColor = $"#{ColorUtility.ToHtmlStringRGB(renderer.material.color)}";
                }
                ConstantForceProps constantForceProps = null;
                ConstantForce constantForce = sceneVRState.Value.GetComponent<ConstantForce>();
                if (constantForce != null){
                    var force = new CoordinatesProperties.Builder()
                    .X(constantForce.force.x)
                    .Y(constantForce.force.y)
                    .Z(constantForce.force.z)
                    .Build();

                    var relativeTorque = new CoordinatesProperties.Builder()
                    .X(constantForce.relativeTorque.x)
                    .Y(constantForce.relativeTorque.y)
                    .Z(constantForce.relativeTorque.z)
                    .Build();

                    constantForceProps = new ConstantForceProps.Builder()
                    .Force(force)
                    .RelativeTorque(relativeTorque)
                    .Build();
                }
                
                ComponentsProperties components = new ComponentsProperties.Builder()
                    .ConstantForce(constantForceProps)
                    .Color(formattedColor)
                    .Build();

                ObjectProperties props = new ObjectProperties.Builder()
                    .Id(sceneVRState.Key)
                    .Tag(sceneVRState.Value.tag)
                    .Name(sceneVRState.Value.name)
                    .Components(components)
                    .Transform(transform)
                    .Build();

                objectsProperties.Add(props);
            }
            Debug.Log("GlobalManager Completed formatting VR states");
            return objectsProperties;
        }

        public void UpdateVRStateProperties(VRStateResponse updatedVRStates)
        {
            foreach (var sceneVRState in vrStateObjects)
            {
                if (!sceneVRState.Value.tag.Contains(updatedVRStates.Tag, StringComparison.OrdinalIgnoreCase)){
                    continue;
                }
                Renderer renderer = sceneVRState.Value.GetComponent<Renderer>();
                ConstantForce constantForce = sceneVRState.Value.GetComponent<ConstantForce>();
                TextMeshPro tmpInputField = sceneVRState.Value.GetComponent<TextMeshPro>();
                Rigidbody rigidBody = sceneVRState.Value.GetComponent<Rigidbody>();
                Debug.Log($"Tag: {sceneVRState.Value.tag}. Updating state of Id: {sceneVRState.Key}");
                foreach (VRProperty vr in updatedVRStates.Properties){
                    if (String.Equals(Config.ColorChange, vr.Name, StringComparison.OrdinalIgnoreCase) && renderer){
                        // Modifies the color of the element
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. Updating Color.");
                        Color updatedColor;
                        ColorUtility.TryParseHtmlString(vr.State, out updatedColor);
                        renderer.material.color = updatedColor;
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. Color assigned: {vr.State}");
                        continue;
                    }else{
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. Does not contain a Color component");
                    }

                    if (String.Equals(Config.LevitationChange, vr.Name, StringComparison.OrdinalIgnoreCase) && constantForce){
                        // Modifies the gravity of the element
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. Updating ConstantForce Y.");
                        Vector3 updatedForce = constantForce.force;
                        updatedForce.y = float.Parse(vr.State);
                        constantForce.force = updatedForce;
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. ConstantForce.Force assigned: {vr.State}");
                        continue;
                    } else {
                            Debug.Log($"Tag: {sceneVRState.Value.tag}. Does not contain a ConstantForce component");
                    }
                            
                    if (String.Equals(Config.RotationChange, vr.Name, StringComparison.OrdinalIgnoreCase) && constantForce){
                        // Modifies the spinning force of the element
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. Updating Relative Torque X.");
                        Vector3 updatedTorque = constantForce.relativeTorque;
                        updatedTorque.x = float.Parse(vr.State);
                        constantForce.relativeTorque = updatedTorque;
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. ConstantForce.RelativeTorque assigned: {vr.State}");
                        continue;
                    } else {
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. Does not contain a RelativeTorque component");
                    }

                    if (String.Equals(Config.SizeChange, vr.Name, StringComparison.OrdinalIgnoreCase) && rigidBody){
                        // Modifies the size of the element
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. Updating Transform Scale.");
                        Vector3 scale = sceneVRState.Value.transform.localScale;
                        scale.x = scale.x * float.Parse(vr.State);
                        scale.y = scale.y * float.Parse(vr.State);
                        scale.z = scale.z * float.Parse(vr.State);
                        sceneVRState.Value.transform.localScale = scale;
                        // Apply a small force to affect physics
                        rigidBody.AddForce(sceneVRState.Value.transform.forward * 0.01f, ForceMode.Force);
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. Transform.Scale assigned: {vr.State}");
                        continue;
                    }else {
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. Does not contain a RigidBody component");
                    }
                            
                    if (String.Equals(Config.TextChange, vr.Name, StringComparison.OrdinalIgnoreCase) && tmpInputField){
                        // Change displayed text on television (a maximum of 539 continuous characters)
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. Updating Text.");
                        tmpInputField.text = vr.State;
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. tmpInputField.text  assigned: {vr.State}");
                        continue;
                    } else {
                        Debug.Log($"Tag: {sceneVRState.Value.tag}. Does not contain a Text component");
                    }
                }
            }
            Debug.Log("VR environment Successfully modified");
        }
    }
}
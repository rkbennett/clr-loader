using System;

using System.IO;

using System.Collections.Generic;
using System.Reflection;

namespace ClrLoader
{
    using static ClrLoader;

    class DomainData : IDisposable
    {
        public delegate int EntryPoint(IntPtr buffer, int size);

        bool _disposed = false;

        public AppDomain Domain { get; }
        public Dictionary<(string, string, string), EntryPoint> _delegates;

        public DomainData(AppDomain domain)
        {
            Domain = domain;
            _delegates = new Dictionary<(string, string, string), EntryPoint>();
        }

        public EntryPoint GetEntryPoint(byte[] assemblyPath, string typeName, string function)
        {
            if (_disposed)
                throw new InvalidOperationException("Domain is already disposed");

            byte[] hashing = null;
            using (System.Security.Cryptography.MD5CryptoServiceProvider md5 = new System.Security.Cryptography.MD5CryptoServiceProvider())
            {
                hashing = md5.ComputeHash(assemblyPath);
            }
            var hash = System.Text.Encoding.Default.GetString(hashing);

            var key = (hash, typeName, function);

            EntryPoint result;

            if (!_delegates.TryGetValue(key, out result))
            {
                
                var assembly = Domain.Load(assemblyPath);
                
                var type = assembly.GetType(typeName, throwOnError: true);
                
                Print($"Loaded type {type}");
                result = (EntryPoint)Delegate.CreateDelegate(typeof(EntryPoint), type, function);

                _delegates[key] = result;
            }

            return result;
        }

        public void Dispose()
        {
            if (!_disposed)
            {
                _delegates.Clear();

                if (Domain != AppDomain.CurrentDomain)
                    AppDomain.Unload(Domain);

                _disposed = true;
            }
        }

    }
}
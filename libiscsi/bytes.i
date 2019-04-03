/* -----------------------------------------------------------------------------
 * Based on cdata.swg and pystrings.py as distributed with Swig
 * ----------------------------------------------------------------------------- */

%fragment("BYTES_FromCharPtrAndSize","header",fragment="SWIG_pchar_descriptor") {
SWIGINTERNINLINE PyObject *
BYTES_FromCharPtrAndSize(const char* carray, size_t size)
{
  if (carray) {
    if (size > INT_MAX) {
      swig_type_info* pchar_descriptor = SWIG_pchar_descriptor();
      return pchar_descriptor ? 
        SWIG_InternalNewPointerObj(%const_cast(carray,char *), pchar_descriptor, 0) : SWIG_Py_Void();
    } else {
      return PyBytes_FromStringAndSize(carray, %numeric_cast(size, Py_ssize_t));
    }
  } else {
    return SWIG_Py_Void();
  }
}
}


%{
typedef struct BYTESCDATA {
    void *data;
    size_t len;
} BYTESCDATA;
%}

%typemap(out,noblock=1,fragment="BYTES_FromCharPtrAndSize") BYTESCDATA {
  %set_output(BYTES_FromCharPtrAndSize($1.data,$1.len));
}
%typemap(in) (const void *indata, size_t inlen) = (char *STRING, size_t SIZE);

%insert("header") {
static BYTESCDATA bytes(void *ptr, size_t nelements)
{
  BYTESCDATA d;
  d.data = (void *) ptr;
  d.len  = nelements;
  return d;
}
}

BYTESCDATA bytes(void *ptr, size_t nelements);

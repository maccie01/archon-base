# React Forms and Validation

Created: 2025-10-13
Last Research: 2025-10-13
Sources: React Hook Form docs, Web Research (Medium, LogRocket, PureCode, DhiWise)

## Overview

Form handling in React has evolved from controlled components with manual validation to specialized libraries. React Hook Form is the current industry standard for 2024-2025, offering superior performance and developer experience.

## Core Principles

1. **Uncontrolled Over Controlled**: React Hook Form uses uncontrolled inputs for better performance
2. **Schema-Based Validation**: Use Zod, Yup, or Joi for type-safe validation
3. **Performance First**: Minimize re-renders during form interaction
4. **Accessibility**: Ensure proper error messaging and ARIA attributes
5. **TypeScript Integration**: Leverage type inference from schemas

## When to Use Each Library

### Use React Hook Form When:
- Building any form in 2024+ (it's the recommended default)
- Need high performance for large forms
- Want minimal re-renders
- Prefer hook-based API
- Need TypeScript integration
- Form has 5+ fields

### Use Formik When:
- Team is already familiar with Formik
- Migrating existing Formik codebase
- Need higher-order component patterns
- Project started before 2023

### Use Plain Controlled Inputs When:
- Very simple forms (1-3 fields)
- Real-time validation on every keystroke is critical
- Learning React fundamentals

## Comparison: React Hook Form vs Formik (2024)

| Feature | React Hook Form | Formik |
|---------|----------------|--------|
| Bundle Size (gzipped) | 12.12 KB | 44.34 KB |
| Dependencies | 0 | 7 |
| Re-renders | Minimal | More frequent |
| Performance | Excellent | Good |
| TypeScript Support | Excellent | Good |
| Learning Curve | Easy | Moderate |
| 2024 Recommendation | **Preferred** | Legacy |

**Verdict**: React Hook Form is the clear winner for new projects in 2024-2025.

## Patterns

### Pattern 1: Basic React Hook Form with Zod

**When to use**: For any new form

**How to implement**: Install react-hook-form and @hookform/resolvers/zod

**Example skeleton**:
```typescript
// TODO: Add example code
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

// Define schema
const userSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  email: z.string().email('Invalid email address'),
  age: z.number().min(18, 'Must be 18 or older'),
})

type UserFormValues = z.infer<typeof userSchema>

const UserForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<UserFormValues>({
    resolver: zodResolver(userSchema),
    defaultValues: {
      username: '',
      email: '',
      age: 18,
    },
  })

  const onSubmit = async (data: UserFormValues) => {
    await api.createUser(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <input {...register('username')} placeholder="Username" />
        {errors.username && <span>{errors.username.message}</span>}
      </div>

      <div>
        <input {...register('email')} type="email" placeholder="Email" />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <input {...register('age', { valueAsNumber: true })} type="number" />
        {errors.age && <span>{errors.age.message}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  )
}
```

**References**:
- [React Hook Form Docs](https://react-hook-form.com/)
- [Zod Documentation](https://zod.dev/)

### Pattern 2: React Hook Form with UI Library (shadcn/ui)

**When to use**: When using component libraries like shadcn/ui, Radix UI

**How to implement**: Use Controller or custom Form components

**Example skeleton**:
```typescript
// TODO: Add example code
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

const UserForm = () => {
  const form = useForm<UserFormValues>({
    resolver: zodResolver(userSchema),
    defaultValues: {
      username: '',
      email: '',
    },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Username</FormLabel>
              <FormControl>
                <Input placeholder="Enter username" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="Enter email" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

**References**:
- [shadcn/ui Form Component](https://ui.shadcn.com/docs/components/form)

### Pattern 3: Dynamic Fields / Field Arrays

**When to use**: For forms with variable number of inputs (e.g., multiple addresses)

**How to implement**: Use useFieldArray

**Example skeleton**:
```typescript
// TODO: Add example code
import { useForm, useFieldArray } from 'react-hook-form'

const DynamicForm = () => {
  const { control, register, handleSubmit } = useForm({
    defaultValues: {
      items: [{ name: '', quantity: 1 }],
    },
  })

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'items',
  })

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {fields.map((field, index) => (
        <div key={field.id}>
          <input {...register(`items.${index}.name`)} placeholder="Name" />
          <input
            {...register(`items.${index}.quantity`, { valueAsNumber: true })}
            type="number"
          />
          <button type="button" onClick={() => remove(index)}>
            Remove
          </button>
        </div>
      ))}

      <button type="button" onClick={() => append({ name: '', quantity: 1 })}>
        Add Item
      </button>

      <button type="submit">Submit</button>
    </form>
  )
}
```

**References**:
- [React Hook Form - useFieldArray](https://react-hook-form.com/docs/usefieldarray)

### Pattern 4: Conditional Fields

**When to use**: When fields appear/disappear based on other field values

**How to implement**: Use watch() to observe field values

**Example skeleton**:
```typescript
// TODO: Add example code
const ConditionalForm = () => {
  const { register, watch, handleSubmit } = useForm()

  const userType = watch('userType')

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <select {...register('userType')}>
        <option value="individual">Individual</option>
        <option value="company">Company</option>
      </select>

      {userType === 'individual' && (
        <>
          <input {...register('firstName')} placeholder="First Name" />
          <input {...register('lastName')} placeholder="Last Name" />
        </>
      )}

      {userType === 'company' && (
        <>
          <input {...register('companyName')} placeholder="Company Name" />
          <input {...register('taxId')} placeholder="Tax ID" />
        </>
      )}

      <button type="submit">Submit</button>
    </form>
  )
}
```

### Pattern 5: File Upload Forms

**When to use**: For forms that include file uploads

**How to implement**: Use register with file input

**Example skeleton**:
```typescript
// TODO: Add example code
const FileUploadForm = () => {
  const { register, handleSubmit } = useForm()

  const onSubmit = async (data) => {
    const formData = new FormData()
    formData.append('file', data.file[0])
    await api.uploadFile(formData)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        type="file"
        {...register('file')}
        accept="image/*"
      />
      <button type="submit">Upload</button>
    </form>
  )
}
```

### Pattern 6: Multi-Step Forms / Wizard

**When to use**: For long forms split into multiple steps

**How to implement**: Use state to track current step, validate each step

**Example skeleton**:
```typescript
// TODO: Add example code
const MultiStepForm = () => {
  const [step, setStep] = useState(1)
  const { register, handleSubmit, trigger, formState: { errors } } = useForm()

  const nextStep = async () => {
    const isValid = await trigger() // Validate current step
    if (isValid) setStep(step + 1)
  }

  const onSubmit = (data) => {
    console.log('Final submission:', data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {step === 1 && (
        <>
          <h2>Step 1: Personal Info</h2>
          <input {...register('firstName')} />
          <input {...register('lastName')} />
          <button type="button" onClick={nextStep}>Next</button>
        </>
      )}

      {step === 2 && (
        <>
          <h2>Step 2: Contact Info</h2>
          <input {...register('email')} />
          <input {...register('phone')} />
          <button type="button" onClick={() => setStep(1)}>Back</button>
          <button type="button" onClick={nextStep}>Next</button>
        </>
      )}

      {step === 3 && (
        <>
          <h2>Step 3: Review</h2>
          {/* Display review */}
          <button type="button" onClick={() => setStep(2)}>Back</button>
          <button type="submit">Submit</button>
        </>
      )}
    </form>
  )
}
```

### Pattern 7: Server-Side Validation Errors

**When to use**: When backend returns validation errors

**How to implement**: Use setError() to display server errors

**Example skeleton**:
```typescript
// TODO: Add example code
const FormWithServerValidation = () => {
  const { register, handleSubmit, setError, formState: { errors } } = useForm()

  const onSubmit = async (data) => {
    try {
      await api.createUser(data)
    } catch (error) {
      // Set server errors
      if (error.response?.data?.errors) {
        Object.entries(error.response.data.errors).forEach(([field, message]) => {
          setError(field, { type: 'server', message })
        })
      }
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
      <button type="submit">Submit</button>
    </form>
  )
}
```

## Validation Libraries

### Zod (Recommended for 2024)
- TypeScript-first schema validation
- Excellent type inference
- Growing ecosystem
- Lightweight

### Yup
- Mature, widely used
- Good documentation
- JavaScript-friendly

### Joi
- Originally for Node.js
- Feature-rich
- Larger bundle size

## Common Mistakes

1. **Controlled Inputs with RHF**: Don't use useState with React Hook Form
2. **Missing Key in Dynamic Fields**: Always use field.id as key
3. **Not Using Schema Validation**: Manual validation is error-prone
4. **Inline Validation Functions**: Define outside component to avoid re-creation
5. **Not Handling Server Errors**: Always integrate backend validation errors
6. **Overcomplicating Simple Forms**: Sometimes a simple controlled input is fine

## Form Accessibility

```typescript
// TODO: Add example code
<div>
  <label htmlFor="email">Email</label>
  <input
    id="email"
    {...register('email')}
    aria-invalid={errors.email ? 'true' : 'false'}
    aria-describedby={errors.email ? 'email-error' : undefined}
  />
  {errors.email && (
    <span id="email-error" role="alert">
      {errors.email.message}
    </span>
  )}
</div>
```

## Tools and Libraries

### Form Libraries
- **React Hook Form**: Modern, performant (recommended)
- Formik: Legacy option
- Final Form: Alternative

### Validation
- **Zod**: TypeScript-first (recommended)
- Yup: Mature, popular
- Joi: Feature-rich

### UI Integration
- shadcn/ui Form components
- Radix UI with React Hook Form
- Material-UI with React Hook Form

## Additional Resources

- [React Hook Form Documentation](https://react-hook-form.com/)
- [Zod Documentation](https://zod.dev/)
- [React Hook Form vs Formik Comparison](https://refine.dev/blog/react-hook-form-vs-formik/)
- [Formik vs React Hook Form (PureCode)](https://blogs.purecode.ai/blogs/formik-vs-react-hook-form)
- [React Hook Form Best Practices](https://www.dhiwise.com/post/choosing-the-right-form-library-formik-vs-react-hook-form)

## Next Steps

- Review [TYPESCRIPT_REACT.md](./TYPESCRIPT_REACT.md) for form type safety
- See [ACCESSIBILITY.md](./ACCESSIBILITY.md) for form accessibility patterns
- Check [ANTIPATTERNS.md](./ANTIPATTERNS.md) for form anti-patterns
